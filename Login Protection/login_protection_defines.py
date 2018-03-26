
'''
Global definitions
'''
MAX_LOGIN_ATTEMPTS = 20

SHELL_CMD_FAILED_PASSWORD_USER  = "cat /var/log/auth.log | grep -a 'sshd.*Failed password for pi'"
SHELL_CMD_FAILED_PASSWORD_ROOT  = "cat /var/log/auth.log | grep -a 'sshd.*Failed password for root'"
SHELL_CMD_ACCEPTED_PASSWORD     = "cat /var/log/auth.log | grep -a 'sshd.*Accepted password'"
