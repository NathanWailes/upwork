import time
import urllib.request
import http.client
import urllib
from county_ids_to_names import county_ids_to_names
from multiprocessing import Pool
import os


def download_reports_for_all_counties(report_types, entry_to_pick_up_after=None):
    """
    :param report_types: These are strings used by the court's API to know which report to pull.  To figure out the
    right value you need to open Chrome Devtools and examine the outgoing request when you do a search for a particular
    report type.
    :param entry_to_pick_up_after: This is a string to compare to, used to pick up in the middle of the job if the
    program was stopped for some reason part-way through.  Ex: "K" or "Ki" or "King"
    :return:
    """
    pool = Pool()
    pool.map(download_court_reports_for_county, [sorted(county_ids_to_names.keys()), report_types,
                                                 entry_to_pick_up_after])


def download_court_reports_for_county(county_id, report_types, entry_to_pick_up_after=None):
    county_name = county_ids_to_names[county_id]
    if not county_name_is_after(county_name, entry_to_pick_up_after):
        return

    for report_type in report_types:
        for year in range(2000, 2011):
            download_report(county_id, report_type, year)


def county_name_is_after(county_name, entry_to_pick_up_after):
    """ If the overall program stops in the middle and we want to pick up later, we can use this function to make sure
    that only the county names that we haven't seen already are getting handled.  This function assumes that your input
    (in this case the list of county names from county_ids_to_names) is sorted alphabetically.

    :param county_name: Examples: Jasper or King or Hopkins
    :param entry_to_pick_up_after:  Example: K or Ki or King
    :return:
    """
    # If no reference value was provided, the user wants to run the program from the beginning of the input.
    if not entry_to_pick_up_after:
        return True

    return sorted([county_name.lower(), entry_to_pick_up_after.lower()])[1] == county_name.lower()


def download_report(county_id, report_type, year):
    to_month = 12 if year != 2010 else 8  # This was specified in the job post: 2010 only has eight months of data.

    url = "https://card.txcourts.gov/oca_ReportViewer.aspx?" + \
          "ReportName=%s&" % report_type + \
          "ddlFromMonth=1&" + \
          "ddlFromYear=%d&" % year + \
          "txtFromMonthField=@FromMonth&" + \
          "txtFromYearField=@FromYear&" + \
          "ddlToMonth=%d&" % to_month + \
          "ddlToYear=%d&" % year + \
          "txtToMonthField=@ToMonth&" + \
          "txtToYearField=@ToYear&" + \
          "ddlCountyPostBack=%d&" % county_id + \
          "txtCountyPostBackField=@CountyID&" + \
          "ddlCourtAfterPostBack=0&" + \
          "txtCourtAfterPostBackField=@CourtID&" + \
          "export=1625"

    # Specify HTTP 1.0 to prevent a chunking error https://stackoverflow.com/q/37816596/4115031
    http.client.HTTPConnection._http_vsn = 10
    http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

    county_name = county_ids_to_names[county_id]
    output_filename = "%s - %d.xls" % (county_name, year)

    if report_type == 'District_Court_Data_Reports/DC_Statewide_Summary_Criminal_89.rpt':
        output_directory = 'district courts'
    elif report_type == 'County-Level_Court_Data_Reports/CC_Statewide_Summary_Criminal_199.rpt':
        output_directory = 'county courts'
    else:
        raise ValueError

    path_to_output_folder = os.path.join(output_directory, county_name)
    if not os.path.exists(path_to_output_folder):
        os.makedirs(path_to_output_folder)

    path_to_output_file = os.path.join(path_to_output_folder, output_filename)
    urllib.request.urlretrieve(url, path_to_output_file)
    print(path_to_output_file)
    time.sleep(1)


# I found the multiprocessing.Pool code at https://stackoverflow.com/a/24398642/4115031
if __name__ == '__main__':
    report_names = ['District_and_Statutory_County_Court/DSC_Felony_Activity_Detail_N.rpt']
    string_to_pick_up_after = None
    download_reports_for_all_counties(report_names, string_to_pick_up_after)
