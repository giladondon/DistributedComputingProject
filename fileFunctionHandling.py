import importlib

__author__ = 'Gilad Barak'

TEMP_FILE_NAME = 'temporary'
PYTHON_ENDING = '.py'


def retrieve_function(function_str_code, function_name):
    file_handler = open(TEMP_FILE_NAME+PYTHON_ENDING, 'w')
    file_handler.write(function_str_code)
    function = importlib.import_module(TEMP_FILE_NAME)

