import logging
import time

from temperature_gui import get_temperature, SENSOR_IDS


logger_to_file = logging.getLogger('get_temperatures_file_logger')
log_file_handler = logging.FileHandler('./get_temperatures.log')
log_file_formatter = logging.Formatter('%(asctime)s %(message)s')
log_file_handler.setFormatter(log_file_formatter)
logger_to_file.addHandler(log_file_handler)
logger_to_file.setLevel(logging.INFO)

logger_to_console = logging.getLogger('get_temperatures_console_logger')
console = logging.StreamHandler()
console_output_formatter = logging.Formatter('%(message)s')
console.setFormatter(console_output_formatter)
logger_to_console.addHandler(console)
logger_to_console.setLevel(logging.INFO)

CONSOLE_OUTPUT_READINGS_PER_MINUTE = 5
FILE_OUTPUT_READINGS_PER_MINUTE = 5


def main():
    """
    1) output all four sensor temps to the console at X rate and 2) output all four sensor temps to a text file with a
    timestamp and at Y rate
    Log in this format: "S1: xxx.xx / S2: xxx.xx / S3: xxx.xx / S4 xxx.xx"

    :return:
    """
    milliseconds_to_wait_between_console_output = int(round((1 / CONSOLE_OUTPUT_READINGS_PER_MINUTE) * 60000))
    milliseconds_to_wait_between_file_output = int(round((1 / CONSOLE_OUTPUT_READINGS_PER_MINUTE) * 60000))
    last_time_there_was_output_to_the_console = get_milliseconds_since_the_epoch()
    last_time_there_was_output_to_the_log_file = get_milliseconds_since_the_epoch()
    while True:
        output_string = ""
        for sensor_number, sensor_id in SENSOR_IDS.items():
            temp_c, temp_f = get_temperature(sensor_id)
            if output_string:
                output_string += ' / '
            output_string += 'S%d %.2f' % (sensor_number, temp_f)
        current_time_in_milliseconds = get_milliseconds_since_the_epoch()
        if current_time_in_milliseconds - last_time_there_was_output_to_the_console > milliseconds_to_wait_between_console_output:
            logger_to_console.info(output_string)
            last_time_there_was_output_to_the_console = current_time_in_milliseconds
        if current_time_in_milliseconds - last_time_there_was_output_to_the_log_file > milliseconds_to_wait_between_file_output:
            logger_to_file.info(output_string)
            last_time_there_was_output_to_the_log_file = current_time_in_milliseconds


def get_milliseconds_since_the_epoch():
    return time.time() * 1000


if __name__ == '__main__':
    main()
