'''
argument_parser.py

Command line parser
'''

import sys
import argparse

from logger import Logger

'''
Global definitions
'''
global_logger = Logger(__file__)


'''
Handle email via command line argument parser
'''
def parse_arguments():

    global_logger.log('Provided command line ', sys.argv)
    
    args = argparse.ArgumentParser()
        
    args.add_argument(
        '--email', 
        dest='email',
        type=str,
        help='Email to receive results', 
        required = False)
        
    args = args.parse_args()

    global_logger.log('Parsed command line ', args)
    
    return args
