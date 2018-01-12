# this is an example of the code I have but it isn't working properly
import csv
from datetime import datetime
import pandas as pd
import dateutil.parser

csv_data = 'input.csv'
output_filename = 'output.csv'

timenow = datetime.now()

epoch = datetime.utcfromtimestamp(0)


def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


def merge_new_data_into_csv(new_data, input_csv_filename, output_csv_filename):

    with open(input_csv_filename) as csvfile:
        reader = csv.DictReader(csvfile)

        existing_data = [row for row in reader]
        existing_data_indexed_by_timestamp = {}

        for row in existing_data:
            datetime_of_row = dateutil.parser.parse(row['timestamp'])

            lookup_value = unix_time_millis(datetime_of_row)
            existing_data_indexed_by_timestamp[lookup_value] = row

        print(next(iter(existing_data_indexed_by_timestamp)))
        fieldnames = set(existing_data[0].keys())
        fieldnames.union(set(new_data[0].keys()))

        for row_of_new_data in new_data:
            datetime_of_row = dateutil.parser.parse(row_of_new_data['timestamp'])
            lookup_value = unix_time_millis(datetime_of_row)

            if lookup_value in existing_data_indexed_by_timestamp.keys():  # If there's a row in the existing data for this time
                for key, value in row_of_new_data.items():
                    if value:  # If there's a value in the new data for this column
                        existing_data_indexed_by_timestamp[lookup_value][key] = value
            else:
                existing_data_indexed_by_timestamp[lookup_value] = row_of_new_data

    data_to_be_exported = list(existing_data_indexed_by_timestamp.values())

    print(data_to_be_exported)

    for index, row in enumerate(data_to_be_exported):
        string_timestamp = row['timestamp']
        datetime_of_row = datetime.strptime(string_timestamp, "%d/%m/%Y %H:%M")
        data_to_be_exported[index]['timestamp'] = datetime_of_row.strftime("%d/%m/%Y %H:%M")

    with open(output_csv_filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for merged_row in existing_data_indexed_by_timestamp.values():
            writer.writerow(merged_row)


if __name__ == '__main__':
    input_csv_filename = 'input.csv'
    output_csv_filename = 'output.csv'

    # First API call
    new_data = [{'timestamp': timenow.strftime("%d/%m/%Y %H:%M"),
                 'col 3': 22313,
                 'col 4': 14699.88,
                 'col 6': 18.7}]
    merge_new_data_into_csv(new_data, input_csv_filename, output_csv_filename)

    # Second API call
    new_data = [{'timestamp': timenow.strftime("%d/%m/%Y %H:%M"),
                 'col 1': 22313,
                 'col 2': 14699.88,
                 'col 5': 18.7}]
    merge_new_data_into_csv(new_data, output_csv_filename, output_csv_filename) # Note the input CSV is the previous API call's output CSV path
