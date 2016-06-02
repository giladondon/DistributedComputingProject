import socket
import select
import marshal
from random import getrandbits

__author__ = 'Gilad Barak'

BIT_VALUE = 128


def get_new_feature():
    """
    Gets new feature from webApp
    :return : [trim function, map function, reduce function]
    """
    pass


def database_assign_feature(file_handler, feature):
    """
    :param file_handler: an open for reading an writing marshaled database file(object marshaled must be dictionary)
    :param feature: [trim function, map function, reduce function]
    :return hash_code: generated code for function
    """
    hash_code = getrandbits(BIT_VALUE)
    database = marshal.load(file_handler)
    database[hash_code] = feature
    marshal.dump(database, file_handler)
    return hash_code


def harness_nodes_dc(nodes, machine_count):
    """
    :param nodes: all nodes currently connected
    :param machine_count: machines number needed for operation
    :return : list of nodes harnessed for operation
    """
    pass


def initiate_server():
    pass


def main():
    pass