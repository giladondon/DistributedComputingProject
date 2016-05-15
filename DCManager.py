from DCProtocol import *
from random import sample
import select

__author__ = 'Gilad Barak'

HKB = 512


class DCManager(object):
    """
    DCServer is a python implementation of a Distributed Computing Manager (Server).
    By using DCServer - managing a Distributed Computing Mechanism is made easier.
    """
    def __init__(self, reduce_func, map_func, trim_func, parameters, nodes, machines_count):
        """
        :param reduce_func: function that takes all nodes responses and makes one full answer
        :param map_func: function to work on every worker computer as distributed
        :param trim_func: function that explains how to trim parameters into little ranges - returns list
        :param parameters: parameters for server function to work on
        :param nodes: a list of available to read & write nodes
        :param machines_count: count of machines to work on current job
        """
        self.response_stock = []
        self.reduce_func = reduce_func
        self.lil_missions = trim_func(parameters, machines_count)
        self.nodes = nodes
        self.working_nodes = sample(nodes, machines_count)
        self.map_func = map_func

    def send_lil_missions(self):
        work_log = {}
        for index in range(self.nodes):
            DCMProtocol(self.map_func, self.lil_missions[index], self.nodes[index]).send_map_func()
            work_log[self.nodes[index]] = self.lil_missions[index]

        return work_log

    def get_responses(self):
        read_list, write_list, error_list = select.select(self.working_nodes, [], [])
        for node in read_list:
            self.response_stock.append()

    def run(self):
        work_log = self.send_lil_missions()

        # getting responses 1 by 1, handling fall outs, putting in response_stock

        # reduce and return answer