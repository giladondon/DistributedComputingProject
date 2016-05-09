import socket
import marshal
import types

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


if __name__ == '__main__':
    main()