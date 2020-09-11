"""
Project Overview: The deliverable will be a python Raspberry Pi python app which needs a simple graphical user
interface. We have a server room in our office and our current method is checking the temperature. We would prefer a
simple Raspberry Pi app we can load on an existing Raspberry Pi which we have in the room already for another purpose.
We need the app to display the temperatures on the GUI and send an email if a certain threshold is reached.

Sensor:
- 4x temperature probes
- 30-120x temperature readings per minute (Needs to be easily adjustable in code)

Parameters:
- Each of the 4 sensors needs two THRESHOLDS I can change individually (i.e. sensor 1 becomes yellow at 80 deg, becomes
red at 85 deg, sensor 2 becomes yellow at 82 deg, etc...)
- Each sensor needs one threshold which sends an email (i.e. sensor 1 email at 82 deg, sensor 2 email at 84 deg, etc...)

Graphical User Interface:
GUI should have 4 sensors that can be gray circles, 2x2 grid is fine. I want to be able to specify a range for each
temperature (each can be different) which when the temp from sensor falls within it is either green, yellow or red.
Also I want a setting where I can send an email if it hits a certain threshold.
"""
import logging
import os
import time
from datetime import datetime, timedelta
from random import randint

import PySimpleGUI as sg

# Things you are likely to want to change:
import sendgrid as sendgrid
from sendgrid import Email, Content, Mail, SendGridAPIClient

# Make some system calls which are apparently needed to read from the temperature sensors.
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

READINGS_PER_MINUTE = 60
MINUTES_TO_WAIT_BEFORE_SENDING_ANOTHER_EMAIL = 15
THRESHOLDS = {
    'yellow': {
        1: 70,
        2: 68,
        3: 83,
        4: 12
    },
    'red': {
        1: 80,
        2: 88,
        3: 93,
        4: 42
    },
    'pop-up': {
        1: 74,
        2: 72,
        3: 88,
        4: 28
    },
    'email': {
        1: 74,
        2: 72,
        3: 88,
        4: 28
    },
}
SENDGRID_API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
EMAIL_SENDER_DISPLAYED_ADDRESS = 'nathan.siahpush@gmail.com'
EMAIL_SENDER_DISPLAYED_NAME = 'Nathan Siahpush'
EMAIL_RECIPIENT_EMAIL_ADDRESS = 'nathan.wailes@gmail.com'
EMAIL_RECIPIENT_DISPLAYED_NAME = 'Nathan Wailes'
EMAIL_SUBJECT_TEMPLATE = 'Sensor %d has tripped threshold'
EMAIL_CONTENT_TEMPLATE = 'Sensor %d has tripped threshold'

# Things you are less likely to want to change:
TEMPERATURE_TEXT_HEIGHT_IN_LINES = 1
TEMPERATURE_TEXT_WIDTH_IN_CHARACTERS = 10
TEMPERATURE_TEXT_PADDING = 60
GREY_CIRCLE = 'grey circle.png'
GREEN_CIRCLE = 'green circle.png'
YELLOW_CIRCLE = 'yellow circle.png'
RED_CIRCLE = 'red circle.png'
CIRCLE_DIAMETER = 250
SENSOR_NUMBER_PADDING = 64

SENSOR_IDS = {
    1: '01192775d558',
    2: '0119279ced19',
    3: '0119277a237d',
    4: '011927afff0c'
}

last_time_email_was_sent_for_sensor = {
    1: None,
    2: None,
    3: None,
    4: None
}

last_time_new_pop_up_was_created_for_sensor = {
    1: None,
    2: None,
    3: None,
    4: None
}

logger_to_file = logging.getLogger('temperature_gui_logger')
log_file_handler = logging.FileHandler('./temperature_gui.log')
log_file_formatter = logging.Formatter('%(asctime)s %(message)s')
log_file_handler.setFormatter(log_file_formatter)
logger_to_file.addHandler(log_file_handler)
logger_to_file.setLevel(logging.INFO)


def main():
    layout = [
        [
            sg.Text('Sensor 1',
                    key='__SENSOR_1_NUMBER__',
                    size=(8, 1),
                    pad=(SENSOR_NUMBER_PADDING, 0)),
            sg.Text('Sensor 2',
                    key='__SENSOR_2_NUMBER__',
                    size=(8, 1),
                    pad=(SENSOR_NUMBER_PADDING, 0)),
            sg.Text('Sensor 3',
                    key='__SENSOR_3_NUMBER__',
                    size=(8, 1),
                    pad=(SENSOR_NUMBER_PADDING, 0)),
            sg.Text('Sensor 4',
                    key='__SENSOR_4_NUMBER__',
                    size=(8, 1),
                    pad=(SENSOR_NUMBER_PADDING, 0))
         ],
        [
            sg.Image(filename=GREY_CIRCLE,
                     key='__SENSOR_1_TEMPERATURE_IMAGE__'),
            sg.Image(filename=GREY_CIRCLE,
                     key='__SENSOR_2_TEMPERATURE_IMAGE__'),
            sg.Image(filename=GREY_CIRCLE,
                     key='__SENSOR_3_TEMPERATURE_IMAGE__'),
            sg.Image(filename=GREY_CIRCLE,
                     key='__SENSOR_4_TEMPERATURE_IMAGE__')
        ],
        [
            sg.Text('temperature',
                    key='__SENSOR_1_TEMPERATURE_NUMBER__',
                    size=(TEMPERATURE_TEXT_WIDTH_IN_CHARACTERS, TEMPERATURE_TEXT_HEIGHT_IN_LINES),
                    pad=(TEMPERATURE_TEXT_PADDING, 0)),
            sg.Text('temperature',
                    key='__SENSOR_2_TEMPERATURE_NUMBER__',
                    size=(TEMPERATURE_TEXT_WIDTH_IN_CHARACTERS, TEMPERATURE_TEXT_HEIGHT_IN_LINES),
                    pad=(TEMPERATURE_TEXT_PADDING, 0)),
            sg.Text('temperature',
                    key='__SENSOR_3_TEMPERATURE_NUMBER__',
                    size=(TEMPERATURE_TEXT_WIDTH_IN_CHARACTERS, TEMPERATURE_TEXT_HEIGHT_IN_LINES),
                    pad=(TEMPERATURE_TEXT_PADDING, 0)),
            sg.Text('temperature',
                    key='__SENSOR_4_TEMPERATURE_NUMBER__',
                    size=(TEMPERATURE_TEXT_WIDTH_IN_CHARACTERS, TEMPERATURE_TEXT_HEIGHT_IN_LINES),
                    pad=(TEMPERATURE_TEXT_PADDING, 0))
         ],
    ]

    window = sg.Window('Window Title', layout,
                       size=(800, 480),
                       resizable=True,
                       margins=(0, 100),
                       element_justification='center')
    while True:
        output_string = ""
        timeout = int(round((1 / READINGS_PER_MINUTE) * 60000))
        event, values = window.Read(timeout=timeout)
        if event in (None, 'Cancel'):   # if user closes the window or clicks cancel
            break
        elif event == '__TIMEOUT__':
            for sensor_number in range(1, 5):
                temp_c, temp_f = get_temperature(SENSOR_IDS[sensor_number])
                update_the_written_temperature(window, sensor_number, temp_f)
                update_the_temperature_indicator_circle(window, sensor_number, temp_f)
                create_pop_up_for_sensor_if_necessary(sensor_number, temp_f)
                send_email_for_sensor_if_necessary(sensor_number, temp_f)
                if output_string:
                    output_string += ' / '
                output_string += 'S%d %.2f' % (sensor_number, temp_f)
        else:
            print(event)
        logger_to_file.info(output_string)
    window.close()


def get_temperature(sensor_id):
    return randint(20, 30), randint(80, 90)
    # lines = read_temp_raw(sensor_id)
    # while lines[0].strip()[-3:] != 'YES':
    #     time.sleep(0.2)
    #     lines = read_temp_raw(sensor_id)
    # equals_pos = lines[1].find('t=')
    # if equals_pos != -1:
    #     temp_string = lines[1][equals_pos + 2:]
    #     temp_c = float(temp_string) / 1000.0
    #     temp_f = temp_c * 9.0 / 5.0 + 32.0
    #     return temp_c, temp_f


def read_temp_raw(sensor_id):
    device_file = '/sys/bus/w1/devices/28-%s/w1_slave' % sensor_id
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def update_the_written_temperature(window, sensor_number, temperature):
    sensor_temperature_number_key = '__SENSOR_%d_TEMPERATURE_NUMBER__' % sensor_number
    new_text_to_display = '%.1f deg f' % float(temperature)
    window.Element(sensor_temperature_number_key).Update(new_text_to_display)


def update_the_temperature_indicator_circle(window, sensor_number, temperature):
    sensor_temperature_image_key = '__SENSOR_%d_TEMPERATURE_IMAGE__' % sensor_number
    if not temperature:
        window.Element(sensor_temperature_image_key).Update(GREY_CIRCLE)
    elif temperature < THRESHOLDS['yellow'][sensor_number]:
        window.Element(sensor_temperature_image_key).Update(GREEN_CIRCLE)
    elif temperature < THRESHOLDS['red'][sensor_number]:
        window.Element(sensor_temperature_image_key).Update(YELLOW_CIRCLE)
    else:
        window.Element(sensor_temperature_image_key).Update(RED_CIRCLE)


def create_pop_up_for_sensor_if_necessary(sensor_number, temperature):
    if temperature and temperature > THRESHOLDS['pop-up'][sensor_number]:
        last_time_sent = last_time_new_pop_up_was_created_for_sensor[sensor_number]
        now = datetime.now()
        if last_time_sent is None or now - last_time_sent > timedelta(minutes=15):
            message = "Warning! Sensor %d reached %s, over temp!" % (sensor_number, '%.2f' % temperature)
            sg.popup_no_wait(message, non_blocking=True, title=message)
            last_time_new_pop_up_was_created_for_sensor[sensor_number] = now


def send_email_for_sensor_if_necessary(sensor_number, temperature):
    if temperature and temperature > THRESHOLDS['email'][sensor_number]:
        last_time_sent = last_time_email_was_sent_for_sensor[sensor_number]
        now = datetime.now()
        if last_time_sent is None or now - last_time_sent > timedelta(minutes=MINUTES_TO_WAIT_BEFORE_SENDING_ANOTHER_EMAIL):
            send_email(sensor_number)
            last_time_email_was_sent_for_sensor[sensor_number] = now


def send_email(sensor_number):
    print("Sending an email for sensor %d" % sensor_number)
    email_content = EMAIL_SUBJECT_TEMPLATE % sensor_number
    email_subject = EMAIL_SUBJECT_TEMPLATE % sensor_number
    message = Mail(
        from_email=EMAIL_SENDER_DISPLAYED_ADDRESS,
        to_emails=EMAIL_RECIPIENT_EMAIL_ADDRESS,
        subject=email_subject,
        html_content=email_content)
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
