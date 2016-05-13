import marshal
import types
import socket

SEP = ','
DEFAULT_RESULT = ''
HKB = 512
TRUE = 'True'

__author__ = 'Gilad Barak'


class DCSProtocol(object):
    """
    DCSProtocol is a two-sided (server-clients) protocol to be used in DCClient and DCServer.
    DCSProtocol is working as a translator to "Socket's Language" for DCClient and DCServer.
    """
    def __init__(self, map_func, parameters, node):
        """
        :param map_func: function object
        :param parameters: any iterable item that represents a range of numbers
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
        is_successful = marshal.loads(self.node.recv(HKB))
        if is_successful:
            result = marshal.loads(self.node.recv(HKB))
            return result


class DCNProtocol(object):
    """
    DCCProtocol is a two-sided (server-clients) protocol to be used in DCClient and DCServer.
    DCCProtocol is working as a translator to "Socket's Language" for DCClient and DCServer.
    """
    def __init__(self, manager):
        self.server = manager
        self.map_func = types.FunctionType(marshal.loads(manager.recv(HKB)), {})
        self.parameters = marshal.loads(manager.recv(HKB))

    def send_result(self, is_successful, result=None):
        """
        :param result: results from task preformed by client
        :param is_successful: True if task was successful
        """
        self.server.send(is_successful)
        if result:
            self.server.send(marshal.dumps(result))