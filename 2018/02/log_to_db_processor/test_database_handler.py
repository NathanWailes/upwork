import contextlib
import sqlite3
import unittest
from inspect import signature

from utils import remove_file
import os
from database_handler import create_database, add_log_entry_to_db

base_path = './'
path_to_test_database = base_path + 'unittest_database.sqlite'

list_of_database_table_names = ["log_entries"]


class TestCreateDatabase(unittest.TestCase):

    def setUp(self):
        self.tearDownClass()

    @classmethod
    def tearDownClass(cls):
        for file_path in [path_to_test_database]:
            if os.path.isfile(file_path):
                remove_file(file_path)

    def test_database_file_exists_after_db_is_created(self):
        """ You can't rely on attempting to connect to the database as a way of verifying that the db exists, because
        even if create_database() fails, the attempt to connect to it will itself create the database. However, in that
        case the tables will not exist.

        :return:
        """
        self.assertFalse(os.path.exists(path_to_test_database))

        create_database(path_to_test_database)

        # We need to check for the creation of the db file with os.path.exists because the mere act of attempting to
        # connect to the db will create it if it doesn't already exist.
        self.assertTrue(os.path.exists(path_to_test_database))

    def test_tables_exist_after_db_is_created(self):
        create_database(path_to_test_database)

        # See https://stackoverflow.com/a/19524679/4115031 for the pattern used below to open the db.
        with contextlib.closing(sqlite3.connect(path_to_test_database)) as con:  # <-- Auto-close the db connection
            with con as session:  # <-- Auto commit or roll back
                result = session.execute("select name from sqlite_master where type='table';").fetchall()
                self.assertTrue(len(result) == len(list_of_database_table_names))

                for result_row in result:
                    table_name = result_row[0]
                    self.assertIn(table_name, list_of_database_table_names)

    def test_that_log_entries_table_fields_exist(self):
        create_database(path_to_test_database)

        with contextlib.closing(sqlite3.connect(path_to_test_database)) as con:
            with con as session:
                result = session.execute("select * from log_entries;")
                field_name_tuples = result.description

                field_names_listed_in_the_add_entry_function = set([value.name for value in signature(add_log_entry_to_db).parameters.values()])
                assert ("path_to_database" in field_names_listed_in_the_add_entry_function)
                field_names_listed_in_the_add_entry_function.remove("path_to_database")
                field_names_listed_in_the_add_entry_function.add("id")  # Need to add 'id' manually since it isn't one of the parameters passed into the 'add an entry' function.

                for field_name_tuple in field_name_tuples:
                    field_name_actually_in_the_table = field_name_tuple[0]
                    self.assertIn(field_name_actually_in_the_table, field_names_listed_in_the_add_entry_function)

    def test_add_log_entry(self):
        create_database(path_to_test_database)

        add_log_entry_to_db(path_to_test_database, timestamp="2018-01-30 00:00:00.000", log_level="INFO",
                            logging_class="FileRequestObjectLogger")

        with contextlib.closing(sqlite3.connect(path_to_test_database)) as con:
            with con as session:
                result = session.execute("select id, log_level from log_entries order by id desc;").fetchall()
                first_result = result[0]

                self.assertEqual(1, first_result[0])  # id should be the first column, given the order in our query


if __name__ == '__main__':
    unittest.main()
