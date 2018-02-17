import json


def get_distinct_ids_from_events_export(path_to_events_data="events_data.jsonl", path_to_output_file="distinct_ids.txt"):
    unique_distinct_ids = set()

    with open(path_to_events_data) as events_data_file:
        line_of_input = events_data_file.readline()
        while line_of_input:
            json_data_for_event = json.loads(line_of_input)

            distinct_id = json_data_for_event['properties']['distinct_id']

            unique_distinct_ids.add(distinct_id)

            line_of_input = events_data_file.readline()

    with open(path_to_output_file, "w") as outfile:
        for distinct_id in unique_distinct_ids:
            outfile.write(str(distinct_id) + "\n")

    return unique_distinct_ids


if __name__ == "__main__":
    # path_to_test_file = "./sample_events_export.jsonl"
    path_to_test_file = "./example_events_export--large.jsonl"
    get_distinct_ids_from_events_export(path_to_test_file, path_to_output_file="distinct_ids.txt")
