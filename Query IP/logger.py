'''
Logger class for console and file

Python dependencies:

logger
'''

import sys
import logging

from os.path import basename


'''
Logger for writing messages to multiple streams.

TODO: Extend to support severity level and level-based filtering
'''
class Logger:

    def __init__(self, i_name):

        self.file_names = []
        self.format = '%(asctime)s - logger(%(name)s) - %(message)s'
        self.formatter = logging.Formatter(self.format)

        self.create_logger(i_name)
        self.register_global_console()

    def create_logger(self, i_name):

        self.logger_name = i_name
        self.logger = logging.getLogger(i_name)
        self.logger.setLevel(logging.INFO)

    def register_global_console(self):

        self.register_handler(logging.StreamHandler(sys.stdout), logging.DEBUG)

        self.log('Registered console')
        
    def register_global_file(self, i_filename):
        
        logging.basicConfig(filename=i_filename, level=logging.INFO, format=self.format)

    def register_filename(self, i_filename):

        if not self.is_filename_registered(i_filename):
            self.file_names.append(i_filename)
            self.register_handler(logging.FileHandler(i_filename), logging.INFO)

        self.log('Registered file:', i_filename)

    def register_handler(self, i_handler, i_log_level):

        i_handler.setFormatter(self.formatter)
        i_handler.setLevel(i_log_level)
        self.logger.addHandler(i_handler)

    def is_filename_registered(self, i_filename):

        return i_filename in self.file_names

    def log(self, *i_args):
    
        i_args = ' '.join([str(arg) for arg in i_args])
        self.logger.info(i_args)

    def get_logger_name(self):

        return self.logger_name
        
    def create_name_from_filename(self, i_filename):
    
        return basename(i_filename).split('.')[0] + '.log'

