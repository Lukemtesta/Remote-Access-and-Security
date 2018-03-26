'''
network_utilities.py

General utilities for handling network requests
'''

import socket
import requests
import subprocess


'''
Query local network ip from web socket
'''
def get_local_ip():

    return socket.gethostbyname(socket.gethostname())
    
'''
Query public network ip from external server
'''
def get_public_ip():

    return requests.get('http://ipinfo.io/ip').text