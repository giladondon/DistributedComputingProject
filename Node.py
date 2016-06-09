from DCNode import *

__author__ = 'Gilad Barak'

IP_MANAGER = '172.16.4.71'
DCPORT = 9421


def reconnect():
    """
    Reconnects with Manager if node crashes.
    Reconnecting helps this python program to be much more powerful
    """
    manager_socket = socket.socket()
    connected = False
    while not connected:
        try:
            manager_socket.connect((IP_MANAGER, DCPORT))
            return manager_socket
        except Exception:
            pass


def main():
    """
    Waits for orders coming from HARDCODED manager.
    When gets any, starts process and returns answers.
    """
    manager_socket = reconnect()
    print 'Connected! \n'
    while True:
        this_node = DCNode(manager_socket)
        results = this_node.work()
        print "results from node: " + str(results)
        if not results:
            manager_socket = reconnect()

if __name__ == "__main__":
    main()