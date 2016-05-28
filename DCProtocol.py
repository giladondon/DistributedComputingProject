import marshal
import pickle
import types
import socket
import sys
import select
import time

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
        self.is_sent = False

    def is_available_send(self):
        """
        Makes sure node gets data on the other side
        """
        (read_list, write_list, error_list) = select.select([], [self.node], [])
        return self.node in write_list

    def send_map_func(self):
        """
        Sends map function to a node via protocol
        """
        self.send_to_node(self.map_func.func_code)
        print "SENT FUNCTION"
        self.send_to_node(self.parameters)
        print 'SENT PARAMETERS'
        self.is_sent = True

    def wait_till_available(self):
        """
        Waits for node to be available for sending
        """
        ready = self.is_available_send()
        while not ready:
            ready = self.is_available_send()

    def send_to_node(self, data):
        """
        Manages every delivery of data to node, by first sending size
        """
        self.wait_till_available()
        self.node.send(marshal.dumps(sys.getsizeof(data)))
        self.wait_till_available()
        self.node.send(marshal.dumps(data))

    def get_result(self):
        """
        gets results from connected node via protocol
        :return result: results from node, if unsuccessful signal received - returns None
        """
        is_successful = marshal.loads(self.node.recv(HKB))
        self.node.send(marshal.dumps(True))
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
        self.raw_func = self.catch_from_server()
        if not self.is_server_down():
            self.parameters = marshal.loads(self.catch_from_server())
            self.map_func = types.FunctionType(marshal.loads(self.raw_func), {})

    def catch_from_server(self):
        """
        Receive anything from server, by first getting size.
        """
        size = self.server.recv(HKB)
        if size == EMPTY:
            return EMPTY
        size = marshal.loads(size)
        return self.server.recv(size + HKB)

    def send_result(self, is_successful, result=None):
        """
        :param result: results from task preformed by client
        :param is_successful: True if task was successful
        """
        self.server.send(marshal.dumps(is_successful))
        ack = marshal.loads(self.server.recv(HKB))
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