import filecmp
import unittest

import os

import time

base_path = './'
test_log_path = base_path + 'unittest_log.log'


def save_setup_files(test_log_string):
    save_string_to_file(test_log_string, path=test_log_path)


def save_string_to_file(string_to_save, path):
    with open(path, 'w') as outfile:
        outfile.write(string_to_save)


class TestGroupStreamedMessagesIntoOutputFile(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        for file_path in [test_log_path]:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_empty_log_file(self):
        log_data = ""
        save_setup_files(log_data)

        log_entries_as_strings = _get_log_entries_as_strings(test_log_path)

        log_entries = [log_entry for log_entry in log_entries_as_strings]
        self.assertEqual([], log_entries)


def remove_file(path, retries=3, sleep=0.1):
    """ I'm using this to fix an issue where the tests will sometimes fail because one of the CSV files can't be deleted.
    The error it shows is "The process cannot access the file because it is being used by another process"

    Solution from https://stackoverflow.com/a/45447192/4115031
    """
    for i in range(retries):
        try:
            os.remove(path)
        except WindowsError:
            time.sleep(sleep)
        else:
            break
