from DCProtocol import *
from random import sample
import select
import time

__author__ = 'Gilad Barak'

HKB = 512


class DCManager(object):
    """
    DCServer is a python implementation of a Distributed Computing Manager (Server).
    By using DCServer - managing a Distributed Computing Mechanism is made easier.
    """
    def __init__(self, reduce_func, map_func, trim_func, parameters, nodes):
        """
        :param reduce_func: function that takes all nodes responses and makes one full answer
        :param map_func: function to work on every worker computer as distributed
        :param trim_func: function that explains how to trim parameters into little ranges - returns list
        :param parameters: parameters for server function to work on
        :param nodes: a list of available to read & write nodes
        """
        self.response_stock = []
        self.reduce_func = reduce_func
        self.lil_missions = trim_func(parameters, len(nodes))
        for lil_mission in self.lil_missions:
            print 'mission: ' + str(lil_mission) + '\n'
        self.map_func = map_func
        self.working_nodes = self.set_working_nodes(nodes)

    def set_working_nodes(self, nodes):
        """
        :param nodes: working nodes' sockets for distributed computing
        returns a dictionary of {working node : protocol object}
        """
        dict_nodes = {}
        for node in nodes:
            dict_nodes[node] = DCMProtocol(self.map_func, [], node)

        return dict_nodes

    def assign_lil_missions(self):
        """
        Assigns pre-trimmed messages to working nodes of server
        """
        index = 0
        for node in self.working_nodes.keys():
            self.working_nodes[node].parameters = self.lil_missions[index]
            index += 1

        for node in self.working_nodes.keys():
            print str(node) + ": " + str(self.working_nodes[node].parameters) + '\n'

    def send_lil_missions(self):
        """
        Sends all little missions to nodes
        """
        while not self.all_sent():
            print 'IN'
            for node in self.working_nodes.keys():
                (read_list, write_list, error_list) = select.select([node],
                                                                    [node], [])
                for machine in write_list:
                        self.working_nodes[machine].send_map_func()

    def get_responses(self):
        """
        Gets responses from nodes
        """
        while len(self.response_stock) != len(self.lil_missions):
            (read_list, write_list, error_list) = select.select(self.working_nodes.keys(),
                                                                self.working_nodes.keys(), [])
            for node in read_list:
                self.response_stock.append(self.working_nodes[node].get_result())

    def reduce_nodes_answers(self):
        """
        In order to keep server alive, reducing will be checked.
        Runs reduce function, if works returns answer.
        """
        try:
            return self.reduce_func(self.response_stock)

        except Exception:
            return None

    def all_sent(self):
        """
        :return : True if all little missions were sent.
        """
        for node in self.working_nodes.keys():
            if not self.working_nodes[node].is_sent:
                return False
        return True

    def run(self):
        """
        Runs distributed computing precision
        """
        self.assign_lil_missions()

        self.send_lil_missions()

        self.get_responses()

        return self.reduce_nodes_answers()


def reduce_for_summing(numbers):
    bank = 0
    for answer in numbers:
        bank += answer

    return bank


def map_for_summing(numbers):
    bank = 0
    for number in numbers:
        bank += number

    return bank


def trim_for_summing(parameter, machines_count):
    size = len(parameter) / (machines_count-1)
    loc = 0
    sub = []
    while loc+size < len(parameter):
        sub.append(parameter[loc:size+loc])
        loc += size
    sub.append(parameter[loc:])
    return sub


def main():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 9421))
    server_socket.listen(2)
    (client_socket1, client_address1) = server_socket.accept()
    (client_socket2, client_address2) = server_socket.accept()
    (client_socket3, client_address3) = server_socket.accept()
    (client_socket4, client_address4) = server_socket.accept()
    print 'WE ARE GOOD'
    par = range(401)
    nodes = [client_socket1, client_socket2, client_socket3, client_socket4]
    manager = DCManager(reduce_for_summing, map_for_summing, trim_for_summing, par, nodes)
    print "FINAL: " + str(manager.run())
    server_socket.close()

if __name__ == "__main__":
    main()
