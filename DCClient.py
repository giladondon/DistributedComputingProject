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
        self.protocol = DCNProtocol(self.own_socket)

    def work(self):
        """
        Node working on his map function received from manager.
        Sends back to server results of function. If unsuccessful sends appropriate signal
        :return result: result of function, if unsuccessful returns None
        """
        map_function = self.protocol.map_func
        try:
            result = map_function(self.protocol.parameters)
            self.protocol.send_result(True, result=result)
            return result
        except Exception:
            self.protocol.send_result(False)
            return None
