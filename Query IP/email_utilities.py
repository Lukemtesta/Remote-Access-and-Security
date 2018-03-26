'''
Python dependencies

pip install imaplib email
'''

import os
import sys
import email
import smtplib
import imaplib
import datetime
import traceback

from collections import namedtuple

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from logger import Logger

'''
Global definitions
'''
TARGET_DOMAIN   = '@gmail.com'

SMTP_RX_SERVER  = 'imap.gmail.com'
SMTP_RX_PORT    = 993
SMTP_TX_SERVER  = 'smtp.gmail.com'
SMTP_TX_PORT    = 587

SENDER_EMAIL    = 'sendserver4096' + TARGET_DOMAIN
SENDER_PWD      = 'HelloWorld'


global_logger = Logger(__file__)


'''
Email item data structure
'''
EmailContents = namedtuple("Email", "address subject message")


'''
Authenticate email with web server
'''
def open_mailbox(
i_from_email, 
i_from_pwd,
i_smtp_server = SMTP_RX_SERVER):

    try:
        mail  = imaplib.IMAP4_SSL(i_smtp_server)
        mail.login(i_from_email, i_from_pwd)
        mail.select()

    except Exception as e:
        mailbox = None
        global_logger.log('Exception: ', sys.exc_info(), traceback.format_exc())
        global_logger.log('Mailbox failed with an exception.')
        mail = None
    
    return mail
    
'''
Switch to inbox and retrieve email information from an authenticated mailbox
\return email type, email metadata
'''
def get_inbox_metadata(i_mailbox):

    state = False
    data = []

    if i_mailbox is not None:

        state, data = i_mailbox.search(None, 'ALL')

    return state, data
    
'''
Retrieve email id from an authenticated mailbox
'''
def get_inbox_email_ids(i_mailbox):

    _, ret = get_inbox_metadata(i_mailbox)
    
    if len(ret) > 0:
        ret = ret[0].split()
    else:
        ret = []
    
    return ret

    
'''
Retrieve email using id from an authenticated mailbox
'''
def get_email_by_id(i_mailbox, i_id, i_protocol = '(RFC822)'):

    ret = None

    _, data = i_mailbox.fetch(i_id, i_protocol )
    
    for response_part in data:
        if isinstance(response_part, tuple):
            contents = email.message_from_string(response_part[1].decode('utf-8'))
            body = extract_email_text(contents)
            ret = EmailContents(address=contents['from'], subject=contents['subject'], message=body)
            
    return ret
    
'''
Retrieve all emails in inbox from target sender 
'''
def get_inbox_emails_from_sender(i_mailbox, i_sender_filter):

    ret = []

    if i_mailbox is not None:

        email_ids = get_inbox_email_ids(i_mailbox)
        email_ids = filter_ids_by_sender(i_mailbox, email_ids, i_sender_filter)
    
        [ ret.append(get_email_by_id(i_mailbox, id)) for id in email_ids ]
    
    return ret
    
'''
Filter emails by sender
'''
def filter_ids_by_sender(i_mailbox, i_ids, i_sender):

    ret = []
        
    for id in i_ids:
        mailitem = get_email_by_id(i_mailbox, id)
        if i_sender in mailitem.address:
            ret.append(id)
            
    return ret
    
'''
Delete email by id in selected mailbox
'''
def delete_by_id(i_mailbox, i_id):
    
    i_mailbox.store(i_id , '+FLAGS', '(\Deleted)')  
    i_mailbox.expunge()
    
'''
Delete all emails in selected mailbox
'''
def delete_all_emails(i_mailbox):

    [delete_by_id(i_mailbox, id) for id in get_inbox_email_ids(i_mailbox)]
    
'''
Convert email messages to command keys
'''
def extract_message_from_emails(i_emails):

    if len(i_emails) is 0:
        return []

    return [email.message for email in i_emails]

'''
Print the email contents to console
'''
def print_emailcontents(i_mailitem):

    if i_mailitem is not None:
        global_logger.log('Address:', i_mailitem.address)
        global_logger.log('Subject:', i_mailitem.subject)
        global_logger.log('Message:', i_mailitem.message)
    
'''
Get email message from message contents of type email.message
'''
def extract_email_text(i_contents):

    ret = None
    
    for part in i_contents.walk():
        if part.get_content_type() == 'text/plain':
            ret = part.get_payload(decode=True).decode('utf-8').rstrip()
            break
        
    return ret
    
'''
Send email with optional attachments 
'''
def send_mail(
i_send_to, 
i_subject = '', 
i_message = '', 
i_filename = None, 
i_send_from = SENDER_EMAIL,
i_sender_pwd = SENDER_PWD):

    msg = MIMEMultipart()
     
    msg['From'] = i_send_from
    msg['To'] = i_send_to
    msg['Subject'] = i_subject
          
    msg.attach(MIMEText(i_message, 'plain'))
    
    if i_filename is not None:
     
        attachment = open(i_filename, "rb")
     
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % i_filename)
     
        msg.attach(part)
     
    server = smtplib.SMTP(SMTP_TX_SERVER, SMTP_TX_PORT)
    server.starttls()
    server.login(i_send_from, i_sender_pwd)
    text = msg.as_string()
    server.sendmail(i_send_from, i_send_to, text)
    server.quit()
    
   
'''
Send report to author via email
'''
def send_report(i_log_name, i_email, i_report_desc = 'Crash Report'):

    global_logger.log('Sending', i_report_desc, 'to', i_email)
    send_mail(i_email, str(datetime.datetime.now()), i_report_desc, i_log_name)
    
    