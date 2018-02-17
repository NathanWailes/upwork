import json

import os

from collections import defaultdict

from download_events_data import download_events_data
from get_distinct_ids_from_events_export import get_distinct_ids_from_events_export
from download_people_data import download_people_data
from tests.generate_example_events_exports import generate_example_events_export
from tests.generate_example_people_data_export import generate_example_people_data_export


def get_combined_people_and_events_data(api_key, api_secret, path_to_output_file="combined_people_and_events_data.jsonl",
                                        number_of_days_to_go_back=7,
                                        simulate=False, number_of_distinct_ids=10, number_of_events_records=100):
    events_data_filepath = "events_data.jsonl"
    people_data_filepath = "individual_person_data.jsonl"

    # If the user has forgotten to delete an old output file, we need to delete it.
    if os.path.exists(path_to_output_file):
        os.remove(path_to_output_file)

    if simulate:
        generate_example_events_export(events_data_filepath, number_of_events_records, number_of_distinct_ids=number_of_distinct_ids)
    else:
        download_events_data(api_key, api_secret, output_filepath=events_data_filepath, number_of_days_to_go_back=number_of_days_to_go_back)

    # this will both save the distinct ids to a file as well as return them as a set
    distinct_ids = get_distinct_ids_from_events_export(path_to_events_data=events_data_filepath, path_to_output_file="distinct_ids.txt")

    distinct_ids_to_events_data_file_line_indices = get_distinct_ids_to_events_data_file_line_indices(events_data_filepath)

    for distinct_id in distinct_ids:
        # We're going to query Mixpanel for just the People data for this one distinct_id
        if simulate:
            generate_example_people_data_export(people_data_filepath, distinct_id)
        else:
            download_people_data(api_key, api_secret, distinct_ids, output_filepath=people_data_filepath)

        with open(people_data_filepath) as people_data_file:
            people_data = json.loads(people_data_file.read())

        # Now get the events data for this person
        events_for_this_distinct_id = []
        with open(events_data_filepath) as events_data_file:
            for index, line in enumerate(events_data_file):
                if index in distinct_ids_to_events_data_file_line_indices[distinct_id]:
                    events_for_this_distinct_id.append(json.loads(line))

        # Combine the events data with the person data
        assert(len(people_data['results']) == 1)
        distinct_id_data = people_data['results'][0]
        distinct_id_data['events'] = events_for_this_distinct_id

        # Append the result to a jsonl file.
        with open(path_to_output_file, 'a') as output_file:
            output_file.write(json.dumps(distinct_id_data) + '\n')


def get_distinct_ids_to_events_data_file_line_indices(events_data_filepath):
    # get a mapping of line #s in the events data to distinct_ids so that we don't need to run json.loads() for each
    # line of the events data file, *for each distinct_id*, which takes a *lot* of time (I found out the hard way).
    distinct_ids_to_events_data_file_line_indices = defaultdict(set)
    with open(events_data_filepath) as events_data_file:
        for index, line in enumerate(events_data_file):
            line_data = json.loads(line)

            distinct_ids_to_events_data_file_line_indices[line_data['properties']['distinct_id']].add(index)

    return distinct_ids_to_events_data_file_line_indices


if __name__ == "__main__":
    api_key = ""
    api_secret = ""
    path_to_output_file = "./combined_people_and_events_data.jsonl"

    # For testing:
    # import cProfile
    # cProfile.run('get_combined_people_and_events_data(api_key=api_key, api_secret=api_secret, '
    #                                                       'path_to_output_file=path_to_output_file, '
    #                                                       'simulate=True, number_of_distinct_ids=2, '
    #                                                       'number_of_events_records=2)')

    get_combined_people_and_events_data(api_key=api_key, api_secret=api_secret, path_to_output_file=path_to_output_file,
                                        number_of_days_to_go_back=1)
