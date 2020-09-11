import base64
import csv
import re
import shutil
import time
from datetime import date, timedelta, datetime, timezone
import pickle
import os.path
from tkinter.messagebox import askyesno

import dateutil
from Scripts.pdf2txt import extract_text
from dateutil import parser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from PyPDF2 import PdfFileWriter, PdfFileReader

from tabula.wrapper import read_pdf

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']  # Delete the file token.pickle when you change the scopes.

EXPECTED_SENDER_EMAIL_ADDRESS = 'hcvstatement@thecha.org'
TEXT_WHICH_EMAILS_OF_INTEREST_ALWAYS_AND_UNIQUELY_CONTAIN = 'CHA Housing Assistance Payment'


def download_and_convert_gmail_attachments_to_csv():
    gmail_credentials = get_gmail_credentials()
    gmail_service = build('gmail', 'v1', credentials=gmail_credentials)

    path_to_the_desired_output_directory = get_the_path_to_the_desired_output_directory()

    email_ids = get_ids_of_all_recent_emails(gmail_service)
    for email_id in email_ids:
        email = gmail_service.users().messages().get(userId='me', id=email_id).execute()
        if email_is_from_the_correct_sender(email) and email_has_the_correct_subject_format(email):
            for part in email['payload']['parts']:
                if 'filename' in part.keys() and part['filename'].endswith('pdf'):
                    download_save_and_convert_attachment(gmail_service, email, email_id, part['body']['attachmentId'],
                                                         part['filename'], path_to_the_desired_output_directory)
                elif 'parts' in part.keys():
                    for sub_part in part['parts']:
                        if 'filename' in sub_part.keys() and sub_part['filename'].endswith('pdf'):
                            download_save_and_convert_attachment(gmail_service, email, email_id, sub_part['body']['attachmentId'],
                                                                 sub_part['filename'], path_to_the_desired_output_directory)


def get_gmail_credentials():
    """ Code from https://developers.google.com/gmail/api/quickstart/python?authuser=6

    :return:
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def get_the_path_to_the_desired_output_directory():
    from tkinter.filedialog import askdirectory

    return askdirectory()


def get_ids_of_all_recent_emails(service):
    desired_date_as_a_string = input("Please specify the date you'd like emails for (use this format: "
                                     "YYYY/MM/DD):\n")

    local_timezone = dateutil.tz.tzlocal()
    local_offset = local_timezone.utcoffset(datetime.now(local_timezone))
    local_offset = int(local_offset.total_seconds() / 3600)
    local_offset_as_a_string = str(local_offset)
    if local_offset >= 0:
        local_offset_as_a_string = "+" + local_offset_as_a_string

    desired_date_as_a_string = desired_date_as_a_string.replace('/', '-') + "T12:00:00" + local_offset_as_a_string

    desired_date = parser.parse(desired_date_as_a_string)
    the_day_after = desired_date + timedelta(1)

    query = "before: {0} after: {1}".format(int(round(the_day_after.timestamp())), int(round(desired_date.timestamp())))

    response = service.users().messages().list(userId='me',
                                               q=query).execute()

    return [message_info['id'] for message_info in response['messages']]


def email_is_from_the_correct_sender(email):
    email_sender = get_who_the_email_is_from(email)
    email_is_from_the_correct_sender = EXPECTED_SENDER_EMAIL_ADDRESS.lower() in email_sender.lower()
    if email_is_from_the_correct_sender:
        return email_is_from_the_correct_sender
    #return EXPECTED_SENDER_EMAIL_ADDRESS.lower() in email_sender.lower()


def email_has_the_correct_subject_format(email):
    email_subject = get_email_subject(email)
    return TEXT_WHICH_EMAILS_OF_INTEREST_ALWAYS_AND_UNIQUELY_CONTAIN.lower() in email_subject.lower()


def get_email_subject(email):
    for header in email['payload']['headers']:
        if header['name'] == 'Subject':
            return header['value']


def get_who_the_email_is_from(email):
    for header in email['payload']['headers']:
        if header['name'] == 'From':
            return header['value']


def download_save_and_convert_attachment(gmail_service, email, email_id, attachment_id, attachment_filename, path_to_output_directory):
    attachment = gmail_service.users().messages().attachments().get(userId='me', messageId=email_id,
                                                                    id=attachment_id).execute()
    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

    output_folder_name = 'HCV Statements %s' % get_email_date(email).strftime('%Y.%m.%d')
    path_to_output_directory = os.path.join(path_to_output_directory, output_folder_name)

    if not os.path.exists(path_to_output_directory):
        os.makedirs(path_to_output_directory)

    path_to_output_file = os.path.join(path_to_output_directory, attachment_filename)
    print(path_to_output_file)

    if os.path.exists(path_to_output_file):
        if get_user_permission_to_overwrite_an_existing_file():
            pass
        else:
            return

    with open(path_to_output_file, 'wb') as outfile:
        outfile.write(file_data)

    convert_attachment_to_csv(path_to_output_file)


def get_email_date(email):
    for header in email['payload']['headers']:
        if header['name'] == 'Date':
            return parser.parse(header['value'])


def get_user_permission_to_overwrite_an_existing_file():
    return askyesno("Overwrite existing file", "A file with the same name already exists in the output "
                                               "directory.  Do you want to overwrite it?")


def convert_attachment_to_csv(path_to_attachment):
    path_to_the_temp_folder = get_the_path_to_the_temp_folder(path_to_attachment)
    prepare_the_temp_folder(path_to_the_temp_folder)
    split_the_attachment_into_one_page_pdfs(path_to_attachment, path_to_the_temp_folder)

    dict_of_pdf_data_ready_to_be_saved_to_a_csv = get_pdf_data_from_the_one_page_pdfs(path_to_the_temp_folder)

    write_pdf_data_to_a_new_csv_file(path_to_attachment, dict_of_pdf_data_ready_to_be_saved_to_a_csv)

    remove_the_temp_folder_and_the_files_it_contains(path_to_the_temp_folder)


def get_the_path_to_the_temp_folder(path_to_attachment):
    path_to_the_containing_folder = os.path.dirname(path_to_attachment)
    path_to_the_temp_folder = os.path.join(path_to_the_containing_folder, 'tmp')
    return path_to_the_temp_folder


def prepare_the_temp_folder(path_to_the_temp_folder):
    if os.path.exists(path_to_the_temp_folder):
        shutil.rmtree(path_to_the_temp_folder)

    if not os.path.exists(path_to_the_temp_folder):
        os.mkdir(path_to_the_temp_folder)


def split_the_attachment_into_one_page_pdfs(path_to_attachment, path_to_the_temp_folder):
    input_pdf = PdfFileReader(open(path_to_attachment, "rb"))

    for i in range(input_pdf.numPages):
        output = PdfFileWriter()
        output.addPage(input_pdf.getPage(i))

        output_filename = "%d.pdf" % i
        path_to_the_output_file = os.path.join(path_to_the_temp_folder, output_filename)
        with open(path_to_the_output_file, "wb") as outputStream:
            output.write(outputStream)


def remove_the_temp_folder_and_the_files_it_contains(path_to_the_temp_folder):
    if os.path.exists(path_to_the_temp_folder):
        shutil.rmtree(path_to_the_temp_folder)


def get_pdf_data_from_the_one_page_pdfs(path_to_the_temp_folder):
    output_table_data = []
    statement_level_data = None

    last_row_type = None
    last_header_row_type = None

    for index, filename in enumerate(os.listdir(path_to_the_temp_folder)):
        path_to_the_current_page = os.path.join(path_to_the_temp_folder, filename)

        if index == 0:  # If we're looking at the first page, grab the statement-level data like Vendor Name, etc.
            statement_level_data = get_statement_level_data(path_to_the_temp_folder, path_to_the_current_page)

        current_page_table_data = read_pdf(path_to_the_current_page, output_format='json')
        if current_page_table_data:
            # The program returns a list because it supports finding multiple tables per page.  And it returns the
            # actual data in a 'data' key because it also returns info like how big the table was on the page.  But we
            # aren't interested in any of that so we're just going to go straight for what we want:
            current_page_table_data = current_page_table_data[0]['data']

            for input_row in current_page_table_data:
                input_row_first_cell_value = input_row[0]['text']
                if input_row_first_cell_value == 'Tenant ID':
                    last_header_row_type = last_row_type = 'TENANT_ID_ETC_HEADER_ROW'
                    continue
                elif input_row_first_cell_value == 'Contract Rent':
                    last_header_row_type = last_row_type = 'CONTRACT_RENT_ETC_HEADER_ROW'
                    continue
                elif last_header_row_type == 'TENANT_ID_ETC_HEADER_ROW' \
                        and last_row_type == 'TENANT_ID_ETC_HEADER_ROW':

                    payment_number, check_date = input_row[3]['text'].split(' ')

                    new_output_row = {
                        'tenant_id': input_row[0]['text'],
                        'tenant_name': input_row[1]['text'],
                        'unit_address': input_row[2]['text'],
                        'payment_number': payment_number,
                        'check_date': check_date
                    }
                    output_table_data.append(new_output_row)
                    last_row_type = 'TENANT_ID_ETC_VALUES_ROW'
                    continue
                elif last_header_row_type == 'TENANT_ID_ETC_HEADER_ROW' \
                        and last_row_type == 'TENANT_ID_ETC_VALUES_ROW':
                    output_row_to_add_onto = output_table_data[-1]

                    # The order of headers below *MUST* match the order in the actual PDF.
                    for index, header in enumerate(['tenant_id', 'tenant_name', 'unit_address', 'payment_number',
                                                    'check_date']):
                        if index in [3, 4]:
                            # The payment number and check date should never go onto a second line and the parser
                            # unfortunately combines their two columns into one, so to avoid an error we'll just skip it
                            continue

                        if input_row[index]['text']:
                            output_row_to_add_onto[header] += ' ' + input_row[index]['text']

                    last_row_type = 'TENANT_ID_ETC_VALUES_ROW'
                    continue
                elif last_header_row_type == 'CONTRACT_RENT_ETC_HEADER_ROW' \
                        and last_row_type == 'CONTRACT_RENT_ETC_HEADER_ROW':
                    output_row_to_add_onto = output_table_data[-1]
                    output_row_to_add_onto.update({
                        'contract_rent': input_row[0]['text'],
                        'tenant_rent': input_row[1]['text'],
                        'hap_amount': input_row[2]['text'],
                        'description': input_row[3]['text'],
                    })
                    last_row_type = 'CONTRACT_RENT_ETC_VALUES_ROW'
                    continue
                elif last_header_row_type == 'CONTRACT_RENT_ETC_HEADER_ROW' \
                        and last_row_type == 'CONTRACT_RENT_ETC_VALUES_ROW':
                    output_row_to_add_onto = output_table_data[-1]

                    # The order of headers below *MUST* match the order in the actual PDF.
                    for index, header in enumerate(['contract_rent', 'tenant_rent', 'hap_amount', 'description']):
                        if input_row[index]['text']:
                            output_row_to_add_onto[header] += ' ' + input_row[index]['text']

                    last_row_type = 'CONTRACT_RENT_ETC_VALUES_ROW'
                    continue

    dict_of_pdf_data_ready_to_be_saved_to_a_csv = get_combined_table_level_data_and_statement_level_data(statement_level_data, output_table_data)

    return dict_of_pdf_data_ready_to_be_saved_to_a_csv


def get_combined_table_level_data_and_statement_level_data(statement_level_data, table_level_data):
    for row in table_level_data:
        for data_type in statement_level_data.keys():
            row[data_type] = statement_level_data[data_type]['value']
    return table_level_data


def get_statement_level_data(path_to_the_temp_folder, path_to_the_current_page):
    statement_level_data = {
        'date_of_statement': {
            'regex': r'((?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), \w+ \d{1,2}, \d{4})',
            'value': None
        },
        'vendor_name': {
            'regex': r'Vendor Name: (.*)',
            'value': None,
        },
        'vendor_number': {
            'regex': r'Vendor #: (\w+)',
            'value': None
        }
    }
    path_to_the_html_file = os.path.join(path_to_the_temp_folder, 'text.html')

    # Unfortunately I wasn't able to find a way to use the pdf2txt to directly get the HTML.  The easiest way to use the
    # library (that I found) was to use pdf2txt's extract_text() function to create a new HTML file, which I can then
    # open and read from.
    extract_text(files=[path_to_the_current_page], outfile=path_to_the_html_file).close()

    with open(path_to_the_html_file, 'r') as infile:
        html_source_code = infile.read()

        for data_type in statement_level_data.keys():
            data_regex = statement_level_data[data_type]['regex']
            matches = re.findall(data_regex, html_source_code)
            if matches:
                statement_level_data[data_type]['value'] = matches[0]
    return statement_level_data


def write_pdf_data_to_a_new_csv_file(path_to_attachment, dict_of_pdf_data_ready_to_be_saved_to_a_csv):

    path_to_folder_containing_attachment = os.path.dirname(path_to_attachment)
    attachment_filename_without_extension = os.path.basename(path_to_attachment[:-4])

    path_to_the_output_csv = os.path.join(path_to_folder_containing_attachment,
                                          'data.csv')

    output_csv_file_is_empty = True
    if os.path.exists(path_to_the_output_csv):
        output_csv_file_is_empty = os.stat(path_to_the_output_csv).st_size == 0

    with open(path_to_the_output_csv, 'a', newline='') as outfile:
        field_names = ['Property ID', 'Remarks', 'GL Account ID', 'Debit', 'Credit', 'Description',
                       'File name of statement', 'Date of Statement', 'Vendor #', 'Tenant ID', 'Contract Rent']

        writer = csv.DictWriter(outfile, fieldnames=field_names)

        if output_csv_file_is_empty:
            writer.writeheader()

        for row in dict_of_pdf_data_ready_to_be_saved_to_a_csv:
            writer.writerow({
                'Property ID': row['vendor_name'],
                'Remarks': row['unit_address'],
                'GL Account ID': None,
                'Debit': row['hap_amount'] if float(row['hap_amount']) > 0 else None,
                'Credit': row['hap_amount'] if float(row['hap_amount']) < 0 else None,
                'Description': row['description'],
                'File name of statement': os.path.basename(path_to_attachment),
                'Date of Statement': parser.parse(row['date_of_statement']).date(),
                'Vendor #': row['vendor_number'],
                'Tenant ID': row['tenant_id'],
                'Contract Rent': row['contract_rent']
            })


if __name__ == '__main__':
    download_and_convert_gmail_attachments_to_csv()
    # path_to_attachment = 'C:\\Users\\Nathan\\Desktop\\HCV Statements 2019.07.15\\11264430.pdf'
    # convert_attachment_to_csv(path_to_attachment)
