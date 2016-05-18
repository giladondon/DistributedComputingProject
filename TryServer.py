import socket
import marshal
import types
import time
from DCProtocol import *

__author__ = 'Gilad Barak'


def calc(x):
    return len(x)


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 9421))
    server_socket.listen(2)
    (client_socket, client_address) = server_socket.accept()
    (client_socket1, client_address1) = server_socket.accept()
    print client_socket
    proto = DCMProtocol(calc, [1, 2, 3, 4, 5], client_socket)
    proto.send_map_func()
    a = proto.get_result()
    print a
    proto = DCMProtocol(calc, [1, 2, 3, 4, 5, 6], client_socket1)
    proto.send_map_func()
    a = proto.get_result()
    print a
    server_socket.close()

if __name__ == '__main__':
    main()