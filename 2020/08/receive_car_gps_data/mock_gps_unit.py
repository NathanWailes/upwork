"""
Code based on the example here:
https://pymotw.com/2/socket/tcp.html
"""
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
server_address = (sys.argv[1], 10000)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)

try:
    # IMEI: https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity
    imei = bytearray.fromhex('000F333536333037303432343431303133')
    print('sending IMEI "%s"' % imei)
    sock.sendall(imei)

    amount_received = 0

    """
    After receiving IMEI, server should determine if it would accept data from
    this module. If yes, server will reply to module 01, if not - 00. Note that
    confirmation should be sent as binary packet. I.e. 1 byte 0x01 or 0x00.
    """
    amount_expected = 1
    bytes_to_indicate_whether_to_proceed = sock.recv(2)
    if int.from_bytes(bytes_to_indicate_whether_to_proceed, 'big') == 1:
        print('received a confirmation to proceed')
        packet = bytearray.fromhex('000000000000003608010000016B40D8EA30010000'
                                   '000000000000000000000000000105021503010101'
                                   '425E0F01F10000601A014E00000000000000000100'
                                   '00C7CF')
        sock.sendall(packet)
        received_data = sock.recv(4)
        print(received_data)
        what_the_server_thinks_the_packet_size_is = int.from_bytes(received_data, 'big')
        print('sent packet of length %d, server responded that the packet was of length %d' % (1, what_the_server_thinks_the_packet_size_is))
    else:
        print('Server will not accept a connection from this IMEI.')

finally:
    sock.close()
