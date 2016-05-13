import socket
import marshal
import types

__author__ = 'Gilad'

KB = 1024


def main():
    my_socket = socket.socket()
    my_socket.connect(('192.168.1.84', 23))
    calc_pickled = my_socket.recv(KB)
    code = marshal.loads(calc_pickled)
    func = types.FunctionType(code, {})
    print func(10)
    print marshal.loads(my_socket.recv(KB))

if __name__ == "__main__":
    main()
