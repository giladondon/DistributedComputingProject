import socket
import marshal
import types
from DCProtocol import *

__author__ = 'Gilad Barak'


def calc(x):
    return x*x


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 23))
    server_socket.listen(1)
    (client_socket, client_address) = server_socket.accept()
    proto = DCMProtocol(calc, 10, client_socket)
    proto.send_map_func()
    a = proto.get_result()
    print a
    proto = DCMProtocol(calc, 20, client_socket)
    proto.send_map_func()
    a = proto.get_result()
    print a
    server_socket.close()

if __name__ == '__main__':
    main()