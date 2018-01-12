import codecs
import csv
import re

missing_leading_digit_error_message = "Line does not contain a leading digit: '%s'"


def convert_input_tsv_to_output_tsv(path_to_input_tsv, path_to_output_tsv, path_to_tsv_of_unhandled_edge_cases, delimiter="\t"):
    expected_input_headers = ["Date & time", "User", "Campaign", "Ad Group", "Changes"]
    change_quantity_header = "ChangeQuantity"
    change_type_header = "ChangeType"
    change_description_header = "ChangeDescription"

    input_dictrows = get_headers_and_dictrows_from_input_tsv(path_to_input_tsv, expected_input_headers, delimiter)
    converted_dictrows = get_converted_dictrows_from_input_dictrows(input_dictrows,
                                                                    expected_input_headers,
                                                                    change_quantity_header=change_quantity_header,
                                                                    change_type_header=change_type_header,
                                                                    change_description_header=change_description_header,
                                                                    path_to_tsv_of_unhandled_edge_cases=path_to_tsv_of_unhandled_edge_cases)
    output_converted_dictrows(converted_dictrows, path_to_output_tsv, expected_input_headers,
                                                                    change_quantity_header=change_quantity_header,
                                                                    change_type_header=change_type_header,
                                                                    change_description_header=change_description_header,
                                                                    delimiter=delimiter)


def get_headers_and_dictrows_from_input_tsv(path_to_tsv, expected_input_headers, delimiter):
    with codecs.open(path_to_tsv) as tsvfile:
        reader = csv.reader(tsvfile, delimiter=delimiter)
        # Skip the first row, which just displays the date range of the TSV
        next(reader)

        # The headers should be on the second row, which is the next row queued to be read from the reader.
        actual_headers = [value for value in next(reader)]

        # Stop and notify the user if anything changes with the format of the input.
        for index, actual_header in enumerate(actual_headers):
            assert(actual_header == expected_input_headers[index]), "Expected %s, got %s" % (expected_input_headers[index], actual_header)

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

        # As a preventative measure. "\r\n" is used by the Windows OS
        plaintext_changes.replace('\r\n', '\n')

        changes_cell_value_as_a_list_of_lines = plaintext_changes.split('\n')

        current_change_type = None
        number_of_rows_outputted_for_this_type = 0

        for line in changes_cell_value_as_a_list_of_lines:

            # If this line shows a "change type"...
            if not line.startswith("  "):

                # If this is the first change_type we're seeing for this input row...
                if not current_change_type:
                    assert(number_of_rows_outputted_for_this_type == 0)
                    current_change_type = line
                    continue

                # If we've already seen a change_type but didn't output a row for that change_type, output one now.
                if number_of_rows_outputted_for_this_type == 0:
                    converted_dictrow = {**converted_dictrow_template}
                    converted_dictrow[change_quantity_header] = get_number_of_changes(current_change_type)
                    converted_dictrow[change_type_header] = get_change_type(current_change_type)
                    converted_dictrow[change_description_header] = ""

                    converted_dictrows.append(converted_dictrow)

                    # We *don't* want to 'continue' here. We want to set the new change_type.

                # Otherwise, just update the change_type and go to the next line to look for a description.
                current_change_type = line.strip()
                number_of_rows_outputted_for_this_type = 0
                continue
            else:  # If we're dealing with a non-change_type, it should be treated like a description:
                assert line  # Make sure the line isn't empty (it should never be)

                converted_dictrow = {**converted_dictrow_template}
                converted_dictrow[change_quantity_header] = get_number_of_changes(current_change_type)
                converted_dictrow[change_type_header] = get_change_type(current_change_type)
                converted_dictrow[change_description_header] = line.strip()

                converted_dictrows.append(converted_dictrow)

                number_of_rows_outputted_for_this_type += 1
                continue

        # Need to handle the edge-case of a cell ending with a new change type:
        if number_of_rows_outputted_for_this_type == 0:
            converted_dictrow = {**converted_dictrow_template}
            converted_dictrow[change_quantity_header] = get_number_of_changes(current_change_type)
            converted_dictrow[change_type_header] = get_change_type(current_change_type)
            converted_dictrow[change_description_header] = ""

            converted_dictrows.append(converted_dictrow)
            continue

    return converted_dictrows


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
        number_of_changes_of_this_type = ""

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
        change_type = line_containing_change_type

    return change_type


def output_converted_dictrows(converted_dictrows, path_to_output_tsv, expected_input_headers, change_quantity_header,
                              change_type_header, change_description_header, delimiter):
    with open(path_to_output_tsv, 'w', newline="") as outfile:
        fieldnames = [*expected_input_headers]
        fieldnames.extend([change_quantity_header, change_type_header, change_description_header])

        writer = csv.DictWriter(outfile, delimiter=delimiter, fieldnames=fieldnames)

        writer.writeheader()

        for row in converted_dictrows:
            writer.writerow(row)


if __name__ == '__main__':
    # convert_input_tsv_to_output_tsv('simple_example_input.tsv', 'output.tsv')
    convert_input_tsv_to_output_tsv('example_input2.tsv', 'output.tsv', 'unhandled_edge_cases.tsv')
