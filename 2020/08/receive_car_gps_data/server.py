"""
Code based on the example here:
https://pymotw.com/2/socket/tcp.html

TODO: Switch the event IO stuff to use Codec8 instead of Codec8 Extended
"""
import configparser
import json
import os
import socket
import sys
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, \
    SmallInteger, Binary
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker

import threading
import socketserver


config = configparser.ConfigParser()
config.read('config.ini')
db_username = config['DEFAULT']['db_username']
db_password = config['DEFAULT']['db_password']
db_address = config['DEFAULT']['db_address']
db_port = config['DEFAULT']['db_port']
db_name = config['DEFAULT']['db_name']

engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' % (db_username, db_password, db_address, db_port, db_name))
Session = sessionmaker(bind=engine)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class AvlDataPacket(Base):
    __tablename__ = config['DEFAULT']['db_table_name']

    id = Column(Integer, primary_key=True)
    imei = Column(String(256))
    raw_bytes = Column(Binary)
    timestamp = Column(DateTime)
    priority = Column(SmallInteger)
    longitude = Column(Float)
    latitude = Column(Float)
    altitude = Column(Integer)
    angle = Column(Integer)
    satellites = Column(SmallInteger)
    speed = Column(Integer)
    event_io_id = Column(String(256))
    event_io_records = Column(LONGTEXT)
    db_row_created = Column(DateTime, default=datetime.utcnow)

# Create all tables that haven't yet been created. I think this line needs to be
# after all of the table definitions.
Base.metadata.create_all(engine)


# As of 2020.08.14 they want to allow all IMEIs
ACCEPTABLE_IMEIS = {}

lock_socket = None


def main():
    if os.name != 'nt':  # For local development on a Windows machine
        if not _is_lock_free():
            sys.exit()
    run_server()


def _is_lock_free():
    """ This function makes it so that I can have have this file run non-stop, and if a cron job tries to run it
    when it's already running, it won't run multiple instances at the same time.
    Code taken from https://help.pythonanywhere.com/pages/LongRunningTasks

    :return:
    """
    global lock_socket
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

    # The lock ID should be unique. using your username as a prefix is a convention
    lock_id = "python_tcp_server"
    try:
        lock_socket.bind('\0' + lock_id)
        print("lock is free2")
        return True
    except socket.error:
        # socket already locked, task must already be running
        return False


def run_server():
    HOST = _get_server_name()
    PORT = 10000
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True  # Exit the server thread when the main thread terminates
        server_thread.start()
        print("Server loop running in thread:", server_thread.name)
        server.serve_forever()


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        cur_thread = threading.current_thread()
        imei = self._get_imei()
        print('imei: ' + imei)
        if True or imei in ACCEPTABLE_IMEIS:  # Allow all IMEIs for now.
            self._get_data_from_avl_unit(imei)
        else:
            self._send_notification_to_not_proceed()

    def _get_imei(self):
        """
        First, when module connects to server, module sends its IMEI. First
        comes short identifying number of bytes written and then goes IMEI
        as text (bytes).
        For example, IMEI 356307042441013 would be sent as
        000F333536333037303432343431303133.
        First two bytes denote IMEI length. In this case 0x000F means, that
        IMEI is 15 bytes long.
        """
        imei_length_in_hexadecimal = self.request.recv(2)
        expected_length_of_the_imei = int.from_bytes(imei_length_in_hexadecimal, 'big')
        imei = ''
        while len(imei) < expected_length_of_the_imei:
            incremental_data_received = self.request.recv(40)
            imei += incremental_data_received.decode()
        return imei

    def _get_data_from_avl_unit(self, imei):
        self._send_confirmation_to_proceed_to_send_avl_data_packet()
        packet_as_hex_bytes = self.request.recv(4096)
        number_of_records_in_the_packet = _parse_avl_packet_and_save_its_data_to_the_db(packet_as_hex_bytes, imei)
        self._send_confirmation_of_avl_data_packet_size(number_of_records_in_the_packet)

    def _send_confirmation_to_proceed_to_send_avl_data_packet(self):
        # https://stackoverflow.com/a/16742052/4115031
        self.request.sendall(bytearray.fromhex('01'))

    def _send_confirmation_of_avl_data_packet_size(self,
                                                   number_of_records_in_the_packet):
        print('sending confirmation of avl data packet size: ' + str(
            number_of_records_in_the_packet))
        self.request.sendall(
            bytearray.fromhex(format(number_of_records_in_the_packet, '08X')))

    def _send_notification_to_not_proceed(self):
        self.request.sendall(bytearray.fromhex('00'))  # format(0, '02X').encode()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True  # https://stackoverflow.com/a/35363839/4115031


def _get_server_name():
    if os.name == 'nt':  # For local development on a Windows machine
        return 'localhost'
    try:
        # Bind the socket to the address given on the command line
        server_name = sys.argv[1]
    except IndexError:
        server_name = socket.gethostname()
    return server_name


def _parse_avl_packet_and_save_its_data_to_the_db(packet_as_hex_bytes, imei):
    print('packet in hex form: ' + ' '.join('{:02x}'.format(letter) for letter in packet_as_hex_bytes))
    preamble = packet_as_hex_bytes[:4]
    data_field_length = packet_as_hex_bytes[4:8]
    codec_id = packet_as_hex_bytes[8:9]
    number_of_records_in_the_packet = int.from_bytes(packet_as_hex_bytes[9:10], 'big')
    index_that_avl_data_ends_before = _get_index_that_avl_data_ends_before(data_field_length)
    avl_data = packet_as_hex_bytes[10:index_that_avl_data_ends_before]
    repetition_of_the_number_of_records_in_the_packet = int.from_bytes(packet_as_hex_bytes[index_that_avl_data_ends_before:index_that_avl_data_ends_before + 1], 'big')
    crc_16 = packet_as_hex_bytes[index_that_avl_data_ends_before + 1:index_that_avl_data_ends_before + 4]

    timestamp = avl_data[:8]
    priority = avl_data[8:9]
    gps_element = avl_data[9:24]
    io_element = avl_data[24:]

    longitude = _get_decimal_degrees(gps_element[:4])
    print(longitude)
    latitude = _get_decimal_degrees(gps_element[4:8])
    print(latitude)
    altitude = gps_element[8:10]
    angle = gps_element[10:12]
    satellites = gps_element[12:13]
    speed = gps_element[13:15]

    event_io_id = io_element[:2]
    total_number_of_io_records = int.from_bytes(io_element[2:4], 'big')
    number_of_one_byte_value_records = int.from_bytes(io_element[4:6], 'big')
    current_index_in_the_unparsed_io_records_data = 6
    one_byte_value_records, current_index_in_the_unparsed_io_records_data = _get_io_records(io_records_unparsed_data=io_element,
                                                                              number_of_bytes_of_the_values=1,
                                                                              number_of_records_to_be_parsed=number_of_one_byte_value_records,
                                                                              current_index_in_the_unparsed_data=current_index_in_the_unparsed_io_records_data)

    number_of_two_byte_value_records = int.from_bytes(io_element[current_index_in_the_unparsed_io_records_data:current_index_in_the_unparsed_io_records_data + 2], 'big')
    two_byte_value_records, current_index_in_the_unparsed_io_records_data = _get_io_records(io_records_unparsed_data=io_element,
                                                                              number_of_bytes_of_the_values=2,
                                                                              number_of_records_to_be_parsed=number_of_two_byte_value_records,
                                                                              current_index_in_the_unparsed_data=current_index_in_the_unparsed_io_records_data + 2)

    number_of_four_byte_value_records = int.from_bytes(io_element[current_index_in_the_unparsed_io_records_data:current_index_in_the_unparsed_io_records_data + 2], 'big')
    four_byte_value_records, current_index_in_the_unparsed_io_records_data = _get_io_records(io_records_unparsed_data=io_element,
                                                                              number_of_bytes_of_the_values=4,
                                                                              number_of_records_to_be_parsed=number_of_four_byte_value_records,
                                                                              current_index_in_the_unparsed_data=current_index_in_the_unparsed_io_records_data + 2)

    number_of_eight_byte_value_records = int.from_bytes(io_element[current_index_in_the_unparsed_io_records_data:current_index_in_the_unparsed_io_records_data + 2], 'big')
    eight_byte_value_records, current_index_in_the_unparsed_io_records_data = _get_io_records(io_records_unparsed_data=io_element,
                                                                              number_of_bytes_of_the_values=8,
                                                                              number_of_records_to_be_parsed=number_of_eight_byte_value_records,
                                                                              current_index_in_the_unparsed_data=current_index_in_the_unparsed_io_records_data + 2)

    number_of_custom_length_records = int.from_bytes(io_element[current_index_in_the_unparsed_io_records_data:current_index_in_the_unparsed_io_records_data + 2], 'big')
    custom_valuelength_records = []
    if number_of_custom_length_records:
        custom_valuelength_records, current_index_in_the_unparsed_io_records_data = _get_io_records_with_custom_valuelengths(io_records_unparsed_data=io_element,
                                                                                                               number_of_records_to_be_parsed=number_of_custom_length_records,
                                                                                                               current_index_in_the_unparsed_data=current_index_in_the_unparsed_io_records_data + 2)
    event_io_records = one_byte_value_records + two_byte_value_records + \
                       four_byte_value_records + eight_byte_value_records + \
                       custom_valuelength_records

    timestamp_as_integer = int.from_bytes(timestamp, 'big')
    timestamp_as_datetime = datetime.fromtimestamp(timestamp_as_integer / 1000)
    orm_representation_of_new_packet = AvlDataPacket(
        imei=imei,
        # raw_bytes=packet_as_hex_bytes,
        timestamp=timestamp_as_datetime,
        priority=int.from_bytes(priority, 'big'),
        longitude=longitude,
        latitude=latitude,
        altitude=int.from_bytes(altitude, 'big'),
        angle=int.from_bytes(angle, 'big'),
        satellites=int.from_bytes(satellites, 'big'),
        speed=int.from_bytes(speed, 'big'),
        event_io_id=str(int.from_bytes(event_io_id, 'big')),
        # event_io_records=json.dumps(event_io_records)  TODO: Find out the max size of this field
    )
    session = Session()
    session.add(orm_representation_of_new_packet)
    session.commit()
    return number_of_records_in_the_packet


def _get_index_that_avl_data_ends_before(data_field_length):
    data_field_length_in_number_of_bytes_in_base_10 = int.from_bytes(data_field_length, 'big')
    """
    - We need to multiply the number of bytes by two because each
      byte is two characters.
    - We need to subtract the length of the codec ID and 'number 
      of data 1' because the data field length is calculated
      to include the codec ID field and 'Number of data 1' field.
    """
    length_of_the_codec_id_field_in_bytes = 1
    length_of_the_number_of_data_1_field_in_bytes = 1
    length_of_the_avl_data_in_bytes = data_field_length_in_number_of_bytes_in_base_10 - length_of_the_codec_id_field_in_bytes - length_of_the_number_of_data_1_field_in_bytes
    index_that_avl_data_ends_before = 10 + length_of_the_avl_data_in_bytes - 1  # IDK why but I have to subtract by one to get the example to not have an off-by-one problem
    return index_that_avl_data_ends_before


def _get_decimal_degrees(byte_string):
    """ This function follows the steps outlined at this link for converting
    from a byte string to decimal degrees:
    https://wiki.teltonika-gps.com/view/Codec#Codec_8

    :param byte_string:
    :return:
    """
    # This integer value will be the same as the one we want if the bytes
    # represent a *positive* number, but if the bytes represent a *negative*
    # number then this integer will be wrong until we transform it with the
    # two's complement.
    raw_byte_value_as_integer = int(byte_string.hex(), 16)

    if _input_bytes_represent_a_negative_number(raw_byte_value_as_integer):
        # For an explanation of how the two's complement is used to represent
        # negative numbers using binary, see:
        # https://wiki.python.org/moin/BitwiseOperators
        twos_complement = raw_byte_value_as_integer ^ 0b11111111111111111111111111111111
        coordinate_encoded_as_an_integer = -1 * twos_complement
    else:
        coordinate_encoded_as_an_integer = raw_byte_value_as_integer

    precision = 10000000
    return coordinate_encoded_as_an_integer / precision


def _input_bytes_represent_a_negative_number(raw_byte_value_as_integer):
    """ From the documentation:
    "To determine if the coordinate is negative, convert it to binary format and
    check the very first bit. If it is 0, coordinate is positive, if it is 1,
    coordinate is negative."

    :param byte_string:
    :return:

    # 526993966 is 0001 1111 0110 1001 0100 1010 0010 1110 in binary. Notice the
    # first bit is '0', indicating a positive number.
    >>> _input_bytes_represent_a_negative_number(526993966)
    False

    # 4274921363 is 1111 1110 1100 1110 0001 1111 1001 0011 in binary. Notice
    # the first bit is '1', indicating a negative number.
    >>> _input_bytes_represent_a_negative_number(4274921363)
    True
    """
    # 032b is making sure that we get a 32-character string of binary 1s and 0s.
    # Otherwise leading 0s will be dropped, which we don't want (since we're
    # looking for a leading 0 bit).
    coordinate_as_string_of_binary_values = "{:032b}".format(raw_byte_value_as_integer)
    return coordinate_as_string_of_binary_values[0] == '1'


def _get_io_records(io_records_unparsed_data, number_of_bytes_of_the_values, number_of_records_to_be_parsed, current_index_in_the_unparsed_data):
    io_records = []
    number_of_records_we_have_parsed = 0
    while number_of_records_we_have_parsed < number_of_records_to_be_parsed:
        index_the_id_ends_before = current_index_in_the_unparsed_data + 2
        index_this_record_ends_before = index_the_id_ends_before + number_of_bytes_of_the_values
        io_records.append({
            'id': int.from_bytes(io_records_unparsed_data[current_index_in_the_unparsed_data:index_the_id_ends_before], 'big'),
            'value': int.from_bytes(io_records_unparsed_data[index_the_id_ends_before:index_this_record_ends_before], 'big')
        })
        current_index_in_the_unparsed_data = index_this_record_ends_before
        number_of_records_we_have_parsed += 1
    return io_records, current_index_in_the_unparsed_data


def _get_io_records_with_custom_valuelengths(io_records_unparsed_data, number_of_records_to_be_parsed, current_index_in_the_unparsed_data):
    io_records = []
    number_of_records_we_have_parsed = 0
    while number_of_records_we_have_parsed < number_of_records_to_be_parsed:
        index_the_id_ends_before = current_index_in_the_unparsed_data + 2
        index_the_valuelength_ends_before = current_index_in_the_unparsed_data + 4
        record_id = io_records_unparsed_data[current_index_in_the_unparsed_data:index_the_id_ends_before]
        number_of_bytes_of_the_value = int.from_bytes(io_records_unparsed_data[index_the_id_ends_before:index_the_valuelength_ends_before], 'big')
        index_this_record_ends_before = index_the_valuelength_ends_before + number_of_bytes_of_the_value
        value = io_records_unparsed_data[index_the_valuelength_ends_before:index_this_record_ends_before]
        io_records.append({
            'id': record_id,
            'value': value
        })
        current_index_in_the_unparsed_data = index_this_record_ends_before
        number_of_records_we_have_parsed += 1
    return io_records, current_index_in_the_unparsed_data


if __name__ == '__main__':
    main()
