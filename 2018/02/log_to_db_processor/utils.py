import time
import os

iso_8601_datetime_format = "%Y-%m-%d %H:%M:%S.%f"
pattern_for_log_entry_timestamp = r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+\]"
possible_log_levels = ["DEBUG", "INFO", "WARN", "ERROR"]
possible_http_methods = ["GET", "HEAD", "PUT", "POST"]
possible_auth_mechanisms = ["NONE", "APP", "DASHBOARD", "INVALID", "API", "URI", "INTERNAL"]


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
