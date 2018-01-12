import filecmp
import unittest

import os

import time

from split_tsv_by_indentation import convert_input_tsv_to_output_tsv

base_path = './'
input_tsv_path = base_path + 'unittest_input.tsv'
expected_output_tsv_path = base_path + 'unittest_expected_output.tsv'
actual_output_tsv_path = base_path + 'unittest_actual_output.tsv'
path_to_tsv_of_unhandled_edge_cases = base_path + 'unittest_unhandled_edge_cases.tsv'


def save_setup_files(input_tsv_string, expected_output_tsv_string):
    save_string_to_file(input_tsv_string, path=input_tsv_path)

    save_string_to_file(expected_output_tsv_string, path=expected_output_tsv_path)


def save_string_to_file(string_to_save, path):
    rows = [row.strip() + '\n' for row in string_to_save.split('\n')]
    with open(path, 'w') as outfile:
        outfile.writelines(rows)


def remove_file(path, retries=3, sleep=0.1):
    """ I'm using this to fix an issue where the tests will sometimes fail because one of the TSV files can't be deleted.
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


class TestAssignVlanIdsToRequests(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        for file_path in [input_tsv_path, expected_output_tsv_path, actual_output_tsv_path]:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_successful_nonredundant_request(self):
        input_tsv_data = """Date Range: XXX
                        Date & time`User`Campaign`Ad Group`Changes
                        Dec 31, 2017 11:28:12 PM`user@user.com`Shopping - US``"1 bid adjustment change\r\n  Desktop: Platform bid adjustment changed from +31% to +32%" """
        expected_output_data = """Date & time`User`Campaign`Ad Group`Changes`ChangeQuantity`ChangeType`ChangeDescription
                                  Dec 31, 2017 11:28:12 PM`user@user.com`Shopping - US``"1 bid adjustment change\r\n  Desktop: Platform bid adjustment changed from +31% to +32%" """
        save_setup_files(input_tsv_data, expected_output_data)

        convert_input_tsv_to_output_tsv(path_to_input_tsv=input_tsv_path, path_to_output_tsv=actual_output_tsv_path,
                                        path_to_tsv_of_unhandled_edge_cases=path_to_tsv_of_unhandled_edge_cases,
                                        delimiter="`")

        self.assertTrue(filecmp.cmp(expected_output_tsv_path, actual_output_tsv_path))


if __name__ == '__main__':
    unittest.main()
