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
    def __init__(self, func, calc_area):
        """
        :param func: function object
        :param calc_area: any iterable item that represents a range of numbers
        """
        self.func = marshal.dumps(func.func_code)
        self.calc_area = SEP.join(calc_area)
        self.result = DEFAULT_RESULT
        self.is_successful = False

    def send_task(self, worker):
        """
        :param worker: a ready to write to client reference
        """
        worker.send(self.func)
        worker.send(self.calc_area)

    def recv_result(self, worker):
        """
        :param worker: a ready to receive from client reference
        """
        self.is_successful = worker.recv(HKB)
        if self.is_successful == TRUE:
            self.result = worker.recv(HKB)
            return self.result


class DCCProtocol(object):
    """
    DCCProtocol is a two-sided (server-clients) protocol to be used in DCClient and DCServer.
    DCCProtocol is working as a translator to "Socket's Language" for DCClient and DCServer.
    """
    def __init__(self, is_successful, result=DEFAULT_RESULT):
        """
        :param is_successful: a boolean value - True if calc was successful
        :param result: any type of object that is an answer to the manager task. (Except Function or Classes)
        """
        self.is_successful = str(is_successful)
        self.result = marshal.dumps(result)
        self.task = DEFAULT_RESULT
        self.calc_area = DEFAULT_RESULT

    def send_result(self, manager):
        """
        :param manager: a ready to write to manager server reference
        """
        manager.send(self.is_successful)
        if self.result != DEFAULT_RESULT:
            manager.send()

    def recv_task(self, manager):
        """
        :param manager: a ready to write to manager server reference
        """
        self.task = types.FunctionType(marshal.loads(manager.recv(HKB)), {})
        self.calc_area = manager.recv(HKB).split(SEP)