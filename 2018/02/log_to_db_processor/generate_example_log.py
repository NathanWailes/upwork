from random import randint
from time import sleep
import os
import zipfile


def generate_example_log(path_to_log_file):
    """ This function takes the ~50mb .zip file and gradually extracts log entries from it into a new .log file to
    simulate the gradual addition of log entries to a log file.

    One limitation of it is that it doesn't print the log entries one at a time, but only prints one *line* at a time.
    So if you are testing code that reads from the log file as it is being written to, your code will often run into
    situations where it is being given a "new log entry" from this script which is actually just a continuation of a
    previous log entry.

    :param path_to_log_file:
    :return:
    """
    try:
        os.remove(path_to_log_file)
    except OSError:
        pass

    outfile1 = open(path_to_log_file, 'ab')
    zfile = zipfile.ZipFile('cos.log.zip')
    for finfo in zfile.infolist():
        with zfile.open(finfo) as ifile:
            for line in ifile:
                print(line)
                outfile1.write(line)
                if randint(0, 10) < 5:
                    sleep_time = 1
                    sleep(sleep_time)


if __name__ == "__main__":
    generate_example_log("cos.log")
    print("Finished processing cos.log")
