__author__ = 'Gilad Barak'

"""
3 must functions from Distributed Computing server, allows working on a range of numbers and sum it.
Includes reduce, map and trim function
"""


def reduce_for_summing(numbers):
    """
    :param numbers: a list of integers
    """
    bank = 0
    for answer in numbers:
        bank += answer

    return bank


def map_for_summing(numbers):
    """
    :param numbers: a list of numbers
    """
    bank = 0
    for number in numbers:
        bank += number

    return bank


def trim_for_summing(parameter, machines_count):
    """
    :param parameter: a list of anything
    """
    size = len(parameter) / (machines_count-1)
    loc = 0
    sub = []
    while loc+size < len(parameter):
        sub.append(parameter[loc:size+loc])
        loc += size
    sub.append(parameter[loc:])
    return sub

if __name__ == '__main__':
    for param in trim_for_summing(range(0, 400), 4):
        print '*****' + str(param) + '******'
