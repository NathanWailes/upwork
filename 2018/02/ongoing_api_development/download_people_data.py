from mixpanel_api import Mixpanel


def download_people_data(api_key, api_secret, distinct_ids, output_filepath="individual_person_data.jsonl"):
    api = Mixpanel(
        api_key=api_key,
        api_secret=api_secret,
        endpoint="http://mixpanel.com/api/2.0/engage"
    )
    for distinct_id in distinct_ids:
        parameters = {'selector': '(properties["distinct_id"] == %s)' % distinct_id}

        api.request(params=parameters, output_filepath=output_filepath)


def download_all_people_data(api_key, api_secret, output_filepath="individual_person_data.jsonl"):
    api = Mixpanel(
        api_key=api_key,
        api_secret=api_secret,
        endpoint="http://mixpanel.com/api/2.0/engage"
    )
    parameters = {}

    api.request(params=parameters, output_filepath=output_filepath)


if __name__ == "__main__":
    api_key = ""
    api_secret = ""
    path_to_output_file = "./combined_people_and_events_data.jsonl"
    download_all_people_data(api_key, api_secret, output_filepath="alL_people_data.jsonl")
