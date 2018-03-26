'''
external_space.py

Tool to query local and public ip addresses.
'''

import sys
import argparse
import traceback

from logger import Logger
from argument_parser import parse_arguments

from network_utilities import *
from email_utilities import send_report, send_mail

'''
Global definitions
'''
global_logger = Logger(__file__)


'''
Main entry point
'''
if __name__ == "__main__":

    log_filename = global_logger.create_name_from_filename(__file__)

    global_logger.register_global_file(log_filename)
    global_logger.log('----- Starting -----')
    
    # Parse command line arguments
    cmdargs = parse_arguments()
    
    try:        
        local_ip = get_local_ip()
        public_ip = get_public_ip()
        
        msg = 'Local IP ' + local_ip + ', Public IP ' + public_ip
        global_logger.log(msg)

        if cmdargs.email:
            global_logger.log('Sending email to', cmdargs.email)
            send_mail(cmdargs.email, msg)
	
    except:        
        global_logger.log('Exception: ', sys.exc_info(), traceback.format_exc())
        if cmdargs.email:
            send_report(log_filename, cmdargs.email)
