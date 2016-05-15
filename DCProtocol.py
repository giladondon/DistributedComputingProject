import marshal
import types
import socket

HKB = 512
EMPTY = ""

__author__ = 'Gilad Barak'


class DCMProtocol(object):
    """
    DCSProtocol is a two-sided (server-clients) protocol to be used in DCClient and DCServer.
    DCSProtocol is working as a translator to "Socket's Language" for DCClient and DCServer.
    """
    def __init__(self, map_func, parameters, node):
        """
        :param map_func: function object
        :param parameters: any iterable item that represents a range of numbers
        :param node: socket to node worker
        """
        self.map_func = map_func
        self.parameters = parameters
        self.node = node

    def send_map_func(self):
        """
        Sends map function to a node via protocol
        """
        self.node.send(marshal.dumps(self.map_func.func_code))
        self.node.send(marshal.dumps(self.parameters))

    def get_result(self):
        """
        gets results from connected node via protocol
        :return result: results from node, if unsuccessful signal received - returns None
        """
        is_successful = marshal.loads(self.node.recv(HKB))
        if is_successful:
            result = marshal.loads(self.node.recv(HKB))
            return result
        return None


class DCNProtocol(object):
    """
    DCCProtocol is a two-sided (server-clients) protocol to be used in DCClient and DCServer.
    DCCProtocol is working as a translator to "Socket's Language" for DCClient and DCServer.
    """
    def __init__(self, manager):
        self.server = manager
        self.raw_func = manager.recv(HKB)
        if not self.is_server_down():
            self.map_func = types.FunctionType(marshal.loads(self.raw_func), globals())
            self.parameters = marshal.loads(manager.recv(HKB))

            print "Parameters from DCNProtocol: " + str(self.parameters)

    def send_result(self, is_successful, result=None):
        """
        :param result: results from task preformed by client
        :param is_successful: True if task was successful
        """
        self.server.send(marshal.dumps(is_successful))
        if result:
            self.server.send(marshal.dumps(result))

    def is_server_down(self):
        """
        When server goes down, it automatically sends an empty message to all clients
        function checks if such message was sent.
        """
        if self.raw_func == EMPTY:
            return True
        return False