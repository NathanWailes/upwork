
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


latitude = b'\x1f\x69\x4a\x2e'
print(_get_decimal_degrees(latitude))

longitude = b'\xfe\xce\x1f\x93'
print(_get_decimal_degrees(longitude))
