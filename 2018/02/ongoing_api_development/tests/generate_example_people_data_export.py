"""
See https://mixpanel.com/help/reference/data-export-api#people-analytics for the format of returned people data (it's
the 'Engage' method.)

Return format:
{"page": 0,
 "page_size": 1000,
 "results": [{"$distinct_id": 4,
              "$properties": {"$created": "2008-12-12T11:20:47",
                              "$email": "example@mixpanel.com",
                              "$first_name": "Example",
                              "$last_name": "Name",
                              "$last_seen": "2008-06-09T23:08:40",}}],
 "session_id": "1234567890-EXAMPL",
 "status": "ok",
 "total": 1}
"""
import json
import random


def generate_example_people_data_export(path_to_output_file, distinct_id):
    with open(path_to_output_file, 'w') as outfile:
            example_record = {"page": 0,
                             "page_size": 1,
                             "results": [{"$distinct_id": distinct_id,
                                          "$properties": {"$created": "2008-12-12T11:20:47",
                                                          "$email": "example@mixpanel.com",
                                                          "$first_name": "Example",
                                                          "$last_name": "Name",
                                                          "$last_seen": "2008-06-09T23:08:40",}}],
                             "session_id": "1234567890-EXAMPL",
                             "status": "ok",
                             "total": 1}
            example_record_as_json_text = json.dumps(example_record) + "\n"

            outfile.write(example_record_as_json_text)


if __name__ == "__main__":
    path_to_output_file = "./example_people_data_export.jsonl"
    generate_example_people_data_export(path_to_output_file, 10)
