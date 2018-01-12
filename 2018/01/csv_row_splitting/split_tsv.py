import codecs
import csv
import re

missing_leading_digit_error_message = "Line does not contain a leading digit: '%s'"


def convert_input_tsv_to_output_tsv(path_to_input_tsv, path_to_output_tsv, path_to_tsv_of_unhandled_edge_cases):
    expected_input_headers = ["Date & time", "User", "Campaign", "Ad Group", "Changes"]
    change_quantity_header = "ChangeQuantity"
    change_type_header = "ChangeType"
    change_description_header = "ChangeDescription"

    input_dictrows = get_headers_and_dictrows_from_input_tsv(path_to_input_tsv, expected_input_headers)
    converted_dictrows = get_converted_dictrows_from_input_dictrows(input_dictrows,
                                                                    expected_input_headers,
                                                                    change_quantity_header=change_quantity_header,
                                                                    change_type_header=change_type_header,
                                                                    change_description_header=change_description_header,
                                                                    path_to_tsv_of_unhandled_edge_cases=path_to_tsv_of_unhandled_edge_cases)
    output_converted_dictrows(converted_dictrows, path_to_output_tsv, expected_input_headers,
                                                                    change_quantity_header=change_quantity_header,
                                                                    change_type_header=change_type_header,
                                                                    change_description_header=change_description_header)


def get_headers_and_dictrows_from_input_tsv(path_to_tsv, expected_input_headers):
    with codecs.open(path_to_tsv) as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        # Skip the first row, which just displays the date range of the TSV
        next(reader)

        # The headers should be on the second row, which is the next row queued to be read from the reader.
        actual_headers = [value for value in next(reader)]

        # Stop and notify the user if anything changes with the format of the input.
        for index, actual_header in enumerate(actual_headers):
            assert(actual_header == expected_input_headers[index])

        dict_rows = []

        # All we're doing below is mimicking the behavior of Python's "DictReader" to create a list of rows where each
        # row is a bunch of key-value pairs (header->cell-value). I couldn't find an easy way to use DictReader when
        # the header isn't on the first row of the file.
        for row in reader:
            new_dictrow = {}
            for index, value in enumerate(row):
                header = actual_headers[index]
                new_dictrow[header] = value
            dict_rows.append(new_dictrow)

        # Stop and alert the user if there are no records.
        assert(len(dict_rows))
    return dict_rows


def get_converted_dictrows_from_input_dictrows(input_dictrows,
                                               expected_input_headers,
                                               change_quantity_header,
                                               change_type_header,
                                               change_description_header,
                                               path_to_tsv_of_unhandled_edge_cases):
    converted_dictrows = []
    for input_row in input_dictrows:

        # Copy the input row. We're going to make copies of this if there are multiple changes.
        converted_dictrow_template = {**input_row}
        del converted_dictrow_template["Changes"]  # Delete the key-value pair for the original 'Changes' column

        plaintext_changes = input_row["Changes"]

        plaintext_changes.replace('\r\n', '\n')  # As a preventative measure. "\r\n" is used by the Windows OS

        changes_cell_value_as_a_list_of_lines = [line.strip() for line in plaintext_changes.split('\n')]

        next_line_to_look_at = 0
        while next_line_to_look_at < len(changes_cell_value_as_a_list_of_lines):
            change_type_line = changes_cell_value_as_a_list_of_lines[next_line_to_look_at]  # Ex: "1 bid adjustment change"

            try:
                number_of_changes = get_number_of_changes(change_type_line)
                change_type = get_change_type(change_type_line)

                # Now that we know how many changes there are of a particular type, we need to get their values
                for i in range(number_of_changes):
                    next_line_to_look_at += 1

                    change_description = changes_cell_value_as_a_list_of_lines[next_line_to_look_at]

                    # Add a row to the converted dictrows for this change description.
                    converted_dictrow = {**converted_dictrow_template}
                    converted_dictrow[change_quantity_header] = number_of_changes
                    converted_dictrow[change_type_header] = change_type
                    converted_dictrow[change_description_header] = change_description

                    converted_dictrows.append(converted_dictrow)

            except ValueError as e:
                if missing_leading_digit_error_message[:10] in e.args[0]:
                    if "StatBid" in plaintext_changes or "Customer changed" in plaintext_changes:

                        change_lines = plaintext_changes.split('\n')
                        try:
                            assert(len(change_lines) == 2)
                        except AssertionError:
                            raise ValueError

                        number_of_changes = ""
                        change_type = change_lines[0].strip()
                        change_description = change_lines[1].strip()

                        # We need to bump the next line to look at by one to account for the fact that this edge case
                        # uses two lines. The other bump happens at the end of the 'while' loop.
                        next_line_to_look_at += 1
                    elif "Enhanced CPC disabled" in plaintext_changes:
                        change_lines = plaintext_changes.split('\n')
                        try:
                            assert(len(change_lines) == 1)
                        except AssertionError:
                            raise ValueError

                        number_of_changes = ""
                        change_type = plaintext_changes.strip()
                        change_description = ""

                    else:
                        output_unhandled_edge_case(input_row, path_to_tsv_of_unhandled_edge_cases,
                                                   expected_input_headers,
                                                   change_quantity_header, change_type_header,
                                                   change_description_header)
                        break
                else:
                    output_unhandled_edge_case(input_row, path_to_tsv_of_unhandled_edge_cases, expected_input_headers,
                                               change_quantity_header, change_type_header, change_description_header)
                    break

                converted_dictrow = {**converted_dictrow_template}
                converted_dictrow[change_quantity_header] = number_of_changes
                converted_dictrow[change_type_header] = change_type
                converted_dictrow[change_description_header] = change_description

                converted_dictrows.append(converted_dictrow)

            # Done with this type of change, look at the next line to see if there are more types within this list of
            # lines of changes
            next_line_to_look_at += 1

    return converted_dictrows


def output_unhandled_edge_case(dict_row, path_to_tsv_of_unhandled_edge_cases, expected_input_headers,
                               change_quantity_header, change_type_header, change_description_header):
    with open(path_to_tsv_of_unhandled_edge_cases, 'a', newline="") as outfile:
        fieldnames = [*expected_input_headers]
        fieldnames.extend([change_quantity_header, change_type_header, change_description_header])

        writer = csv.DictWriter(outfile, delimiter="\t", fieldnames=fieldnames)

        writer.writerow(dict_row)



def get_number_of_changes(line_containing_change_type):
    """
    Example input: "1 bid adjustment change"
    Example output: 1

    :param line_containing_change_type: str
    :return: int
    """
    assert(isinstance(line_containing_change_type, str))

    matches = re.match("^(\d+)", line_containing_change_type)
    if matches:
        number_of_changes_of_this_type = int(matches.group(1))
    else:
        raise ValueError(missing_leading_digit_error_message % line_containing_change_type)

    return number_of_changes_of_this_type


def get_change_type(line_containing_change_type):
    """
    Example input: "1 bid adjustment change"
    Example output: "bid adjustment change"

    :param line_containing_change_type: str
    :return: str
    """
    assert(isinstance(line_containing_change_type, str))

    matches = re.match("^\d+([^\n]*)$", line_containing_change_type)
    if matches:
        change_type = matches.group(1).strip()
    else:
        raise ValueError

    return change_type


def output_converted_dictrows(converted_dictrows, path_to_output_tsv, expected_input_headers, change_quantity_header,
                              change_type_header, change_description_header):
    with open(path_to_output_tsv, 'w', newline="") as outfile:
        fieldnames = [*expected_input_headers]
        fieldnames.extend([change_quantity_header, change_type_header, change_description_header])

        writer = csv.DictWriter(outfile, delimiter="\t", fieldnames=fieldnames)

        writer.writeheader()

        for row in converted_dictrows:
            writer.writerow(row)


if __name__ == '__main__':
    # convert_input_tsv_to_output_tsv('simple_example_input.tsv', 'output.tsv')
    convert_input_tsv_to_output_tsv('example_input2.tsv', 'output.tsv', 'unhandled_edge_cases.tsv')
