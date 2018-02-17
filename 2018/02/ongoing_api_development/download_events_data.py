from mixpanel_api import Mixpanel
from datetime import date, timedelta, datetime


def download_events_data(api_key, api_secret, output_filepath="events_data.jsonl", number_of_days_to_go_back=7):
	one_week_ago = date.today() - timedelta(days=number_of_days_to_go_back)
	from_date = str(one_week_ago)
	to_date = str(date.today())

	api = Mixpanel(
		api_key=api_key,
		api_secret=api_secret,
		endpoint="http://data.mixpanel.com/api/2.0/export"
	)

	api.request(params={'from_date': from_date,
						'to_date': to_date
						},
				output_filepath=output_filepath)
