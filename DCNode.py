from DCProtocol import *

__author__ = 'Gilad Barak'


class DCNode(object):
    """
    DCClient is a python implementation of a Distributed Computing Client.
    In other words - a single computer that is working as a part of a bigger calculation mechanism.
    Using DCClient receiving a task from the manager and completing it has never been easier.
    """
    def __init__(self, node_socket):
        """
        :param node_socket: a socket object connected to server side on other end
        """
        self.own_socket = node_socket
        self.connector = DCNProtocol(self.own_socket)

    def work(self):
        """
        Node working on his map function received from manager.
        Sends back to server results of function. If unsuccessful sends appropriate signal
        :return result: result of function, if unsuccessful returns None
        """
        if self.connector.is_server_down():
            print "DOWN"
            return None

        map_function = self.connector.map_func

        try:
            result = map_function(self.connector.parameters)
            print "result form DCNode: " + str(result)
            self.connector.send_result(True, result=result)
            self.connector.send_result(True, result=result)
            return result

        except Exception:
            self.connector.send_result(False)
            return None

if __name__ == "__main__":
    my_socket = socket.socket()
    my_socket.connect(('192.168.1.84', 23))
    node = DCNode(my_socket)
    node.work()
