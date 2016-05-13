import socket
import marshal
import types
import DCServer

__author__ = 'Gilad Barak'


def calc(x):
    return x*x


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 23))
    server_socket.listen(1)
    (client_socket, client_address) = server_socket.accept()
    calc_pickled = marshal.dumps(calc.func_code)
    client_socket.send(calc_pickled)
    try_shit = [1, 2, 3, 'Hello', True]
    client_socket.send(marshal.dumps(try_shit))


if __name__ == '__main__':
    main()