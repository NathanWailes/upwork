import re

import time

import argparse
from datetime import datetime

import os
from pygtail import Pygtail
from generate_example_log import generate_example_log
from utils import pattern_for_log_entry_timestamp, iso_8601_datetime_format, remove_file
from parse_log_entry import get_dict_from_log_entry_as_a_string
from database_handler import create_database, add_log_entry_to_db


def move_log_entries_from_log_file_to_database(path_to_log_file, path_to_database, skip_edge_cases=True):
    create_database(path_to_database)

    while True:
        # The definition of 'log_entries_as_strings' *must* be within the "while" loop in order to have it update as the
        # file is written to.
        log_entries_as_strings = _get_log_entries_as_strings(path_to_log_file)
        for log_entry_as_a_string in log_entries_as_strings:
            try:
                log_entry_dict = get_dict_from_log_entry_as_a_string(log_entry_as_a_string)
            except AssertionError:
                if not skip_edge_cases:
                    raise
                continue
            add_log_entry_to_db(path_to_database,
                                timestamp=log_entry_dict['datetime'].strftime(iso_8601_datetime_format),
                                log_level=log_entry_dict['log_level'],
                                logging_class=log_entry_dict['logging_class'],
                                uri=log_entry_dict['uri'],
                                uri_pattern=log_entry_dict['uri_pattern'],
                                request_uuid=log_entry_dict['request_uuid'],
                                device_uuid=log_entry_dict['device_uuid'],
                                merchant_id=log_entry_dict['merchant_id'],
                                version_id=log_entry_dict['version_id'],
                                request_ip=log_entry_dict['request_ip'],
                                http_method=log_entry_dict['http_method'],
                                http_status=log_entry_dict['http_status'],
                                developer_app_id=log_entry_dict['developer_app_id'],
                                auth_mechanism=log_entry_dict['auth_mechanism'],
                                request_time=log_entry_dict['request_time'],
                                log_statement=log_entry_dict['log_statement'])

            print(log_entry_as_a_string, end="")

        time.sleep(1)


def _get_log_entries_as_strings(path_to_log_file):
    """ The idea here is this: this is a generator function, and every time it is called it will use pygtail to look at
    whatever lines we have not already examined, and read as many lines as necessary until a regex finds a match for a
    string log entry. A match is defined by a timestamp and everything after it (including newlines) until a new
    timestamp is seen (with the match not including the second timestamp).

    Because we're relying on the second timestamp to verify that we have a full time log entry, we need to handle the
    edge case of the last log entry. To do that we're going to rely on the fact that the "for line in pygtail" loop
    will end at the end of the file: if the loop has finished, we must be at the end of the file, and so we can just
    return whatever unreturned text we have from the previous X lines as the final log entry.

    :param path_to_log_file:
    :return:
    """
    string_data_from_file_that_needs_to_be_processed = ""

    for index, line in enumerate(Pygtail(path_to_log_file, every_n=100)):
        string_data_from_file_that_needs_to_be_processed += line

        string_data_from_file_that_needs_to_be_processed = _remove_incomplete_initial_log_entry_rows_from_a_previous_run(string_data_from_file_that_needs_to_be_processed, index)

        if string_data_from_file_that_needs_to_be_processed:
            log_entry_string_pattern = _get_pattern_for_log_entries()
            matches = re.findall(log_entry_string_pattern, string_data_from_file_that_needs_to_be_processed)
            if matches:
                try:
                    assert(len(matches) == 1)
                except:
                    raise
                match = matches[0]

                # Remove the current log entry from the data that needs to be processed, and keep the remaining text.
                string_data_from_file_that_needs_to_be_processed = string_data_from_file_that_needs_to_be_processed[len(match):]
                yield match

    if string_data_from_file_that_needs_to_be_processed:
        # At the end of the file, put out the last log entry
        assert(re.fullmatch(_get_pattern_for_final_log_entry(), string_data_from_file_that_needs_to_be_processed))
        yield string_data_from_file_that_needs_to_be_processed
    else:
        return None


def _remove_incomplete_initial_log_entry_rows_from_a_previous_run(string_data_from_file_that_needs_to_be_processed, index):
    """ Motivation: I was testing _get_log_entries_as_strings() and ran into an issue where the script stopped for some
    reason (maybe an assertion error), and when I ran it again the pygtail offset file was set in the middle of a log
    entry, which messed up the program. This function will hopefully prevent that from being an issue without causing
    any unintended side-effects.

    :param string_data_from_file_that_needs_to_be_processed:
    :param index:
    :return:
    """
    if index < 100:  # check the first 100 rows, although we expect this to only be an issue for maybe 20 rows max
        # If the incomplete data doesn't start with a timestamp, discard it.
        if string_data_from_file_that_needs_to_be_processed and not re.match(r"^\n?" + pattern_for_log_entry_timestamp, string_data_from_file_that_needs_to_be_processed):
            print("Discarding incomplete log entry: %s" % string_data_from_file_that_needs_to_be_processed)
            string_data_from_file_that_needs_to_be_processed = ""
    return string_data_from_file_that_needs_to_be_processed


def _get_pattern_for_log_entries():
    remaining_log_entry_up_to_the_logging_class = r"[\s\S]+?"  # <-- The "?" makes it match only one log entry.
    lookahead_to_next_log_entry_timestamp = r"(?=\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\])"
    pattern = pattern_for_log_entry_timestamp + remaining_log_entry_up_to_the_logging_class + lookahead_to_next_log_entry_timestamp
    return pattern


def _get_pattern_for_final_log_entry():
    """

    Note: You *cannot* assume that the Logging Class will be at the very end of the log entry. Error logs have the stack
    trace at the end.

    :return:
    """
    remaining_log_entry_up_to_the_logging_class = r"[\s\S]+"
    possible_newline_at_the_end = "\n?"
    return pattern_for_log_entry_timestamp + remaining_log_entry_up_to_the_logging_class + possible_newline_at_the_end


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move log entries from a log file to a sqlite database.")
    parser.add_argument("path_to_log_file", nargs=1, metavar="log", type=str,
                        help="Path to the log file to pull log entries from.")
    parser.add_argument("path_to_database", nargs=1, metavar="db", type=str,
                        help="Desired path to the sqlite database. If it doesn't exist yet, it will be created.")

    args = parser.parse_args()

    path_to_log_file = args.path_to_log_file[0]  # "cos.log"
    path_to_database = args.path_to_database[0]  # "./database.sqlite"
    move_log_entries_from_log_file_to_database(path_to_log_file, path_to_database)
