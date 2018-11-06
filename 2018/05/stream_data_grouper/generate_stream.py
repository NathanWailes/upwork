import json
import random
import time
import example_messages

from datetime import datetime, timedelta


def generate_stream(starting_datetime=None, starting_number_of_records=0, messages_per_minute=60,
                    maximum_delay_in_seconds_for_a_record_to_arrive=0, use_full_example_messages=True):
    with open('example_stream.txt', 'a') as outfile:
        if not starting_datetime:
            starting_datetime = datetime.now()

        last_iteration_datetime = None
        number_of_records = 0

        possible_messages = list(get_variable_names_to_values('example_messages').values())

        while True:
            if not last_iteration_datetime:
                current_iteration_datetime = starting_datetime
            else:
                time_til_next_record = 60 / messages_per_minute

                if number_of_records >= starting_number_of_records:
                    time.sleep(time_til_next_record)

                current_iteration_datetime = last_iteration_datetime + timedelta(seconds=time_til_next_record)

            if maximum_delay_in_seconds_for_a_record_to_arrive:
                number_of_seconds_to_delay = random.randint(0, maximum_delay_in_seconds_for_a_record_to_arrive)
                datetime_of_log_entry = current_iteration_datetime - timedelta(seconds=number_of_seconds_to_delay)
            else:
                datetime_of_log_entry = current_iteration_datetime

            current_iteration_datetime_as_string = datetime_of_log_entry.strftime('%Y-%m-%dT%I:%M:%SZ')

            print(current_iteration_datetime_as_string)

            if use_full_example_messages:
                message = random.choice(possible_messages)
            else:
                message = {}

            message['time'] = current_iteration_datetime_as_string

            outfile.write(json.dumps(message) + '\n')
            outfile.flush()

            number_of_records += 1
            last_iteration_datetime = current_iteration_datetime


def get_variable_names_to_values(module_name):
    module = globals().get(module_name, None)
    variable_names_to_values = {}
    if module:
        variable_names_to_values = {key: value for key, value in module.__dict__.items() if not (key.startswith('__') or key.startswith('_'))}
    return variable_names_to_values


if __name__ == '__main__':
    # generate_stream(messages_per_minute=60)

    generate_stream(messages_per_minute=1000, starting_datetime=None, starting_number_of_records=1000,
                    maximum_delay_in_seconds_for_a_record_to_arrive=414, use_full_example_messages=True)
