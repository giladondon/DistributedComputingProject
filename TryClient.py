import socket
import marshal
import types

__author__ = 'Gilad'


def main():
    my_socket = socket.socket()
    my_socket.connect(('192.168.1.84', 23))
    calc_pickled = my_socket.recv()
    code = marshal.loads(calc_pickled)
    func = types.FunctionType(code, {})
    print func(10)

if __name__ == "__main__":
    main()
