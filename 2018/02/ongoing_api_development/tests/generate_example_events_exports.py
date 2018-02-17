import json
import random


def generate_example_events_export(path_to_output_file, number_of_records_to_create, number_of_distinct_ids=1000):
    example_distinct_ids = [number for number in range(number_of_distinct_ids)]

    with open(path_to_output_file, 'w') as outfile:
        for i in range(number_of_records_to_create):
            example_record = {'event': 'Viewed report',
                              'properties': {'distinct_id': random.choice(example_distinct_ids),
                                              'time': 1329263748,
                                               'origin': 'invite',
                                              "origin_referrer": "http://mixpanel.com/projects/",
                                              "$initial_referring_domain": "mixpanel.com",
                                              "$referrer": "https://mixpanel.com/report/3/stream/",
                                              "$initial_referrer": "http://mixpanel.com/",
                                              "$referring_domain": "mixpanel.com", "$os": "Linux",
                                              "origin_domain": "mixpanel.com", "tab": "stream", "$browser": "Chrome",
                                              "Project ID": "3", "mp_country_code": "US"}}
            example_record_as_json_text = json.dumps(example_record) + "\n"

            outfile.write(example_record_as_json_text)


if __name__ == "__main__":
    path_to_output_file = "./example_events_export--large.out"
    generate_example_events_export(path_to_output_file, 500000)
