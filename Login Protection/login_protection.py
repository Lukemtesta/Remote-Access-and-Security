'''
login_protection.py

Tool to monitor login attempts on a Linux machine. Shuts down to close network connection 
if too are attempted
'''

import sys
import time
import argparse
import traceback
import subprocess

from logger import Logger
from argument_parser import parse_arguments

from email_utilities import send_report, send_mail
from login_protection_defines import *

'''
Global definitions
'''
global_logger = Logger(__file__)
    
    
'''
Monitor login attempts
'''
def get_login_attempts():

    data = subprocess.check_output(SHELL_CMD_FAILED_PASSWORD_USER, shell=True)
    data = data.split('ssh2')
    return str(MAX_LOGIN_ATTEMPTS - len(data))
    
'''
Shutdown and email if attempts are too many
'''
def handle_login_attempts(i_attempts, i_email = None):

    if len(data) >= MAX_LOGIN_ATTEMPTS:
    
        if i_email:
            global_logger.log('Sending email to', i_email)
            send_mail(i_email, 'Intrusion Attempt', time.time(), '/var/log/auth.log')

        subprocess.call('sudo shutdown -h now', shell=True)

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

        attempts = get_login_attempts()
        handle_login_attempts(attempts, cmdargs.email)

    except:        
        global_logger.log('Exception: ', sys.exc_info(), traceback.format_exc())
        if cmdargs.email:
            send_report(log_filename, cmdargs.email)
