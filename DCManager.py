from DCProtocol import *
from random import sample

__author__ = 'Gilad Barak'


class DCManager(object):
    """
    DCServer is a python implementation of a Distributed Computing Manager (Server).
    By using DCServer - managing a Distributed Computing Mechanism is made easier.
    """
    def __init__(self, reduce_func, map_func, trim_func, parameters, nodes, machines_count):
        """
        :param reduce_func: function that takes all nodes responses and makes one full answer
        :param trim_func: function that explains how to trim parameters into little ranges
        :param parameters: parameters for server function to work on
        :param nodes: a list of available to read & write nodes
        :param machines_count: count of machines to work on current job
        """
        self.response_stock = []
        self.reduce_func = reduce_func
        self.lil_missions = trim_func(parameters, machines_count)
        self.nodes = sample(nodes, machines_count)
        self.map_func = map_func

    def send_lil_missions(self):
        for index in range(self.nodes):
            DCMProtocol(self.map_func, self.lil_missions[index], self.nodes[index]).send_map_func()

    def run(self):
        self.send_lil_missions()
        # getting responses 1 by 1, handling fall outs, putting in response_stock
        # reduce and return answer