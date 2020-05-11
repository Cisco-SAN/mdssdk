import logging

import paramiko
from time import sleep

from .errors import SSHException

log = logging.getLogger(__name__)


class SSHConnectionException(SSHException):
    pass


class SSHCommandException(SSHException):
    pass


class SSHSession(object):
    """
    Generic SSHSession which can be used to run commands
    """

    def __init__(self, host, username, password, timeout=60):
        """
        Establish SSH Connection using given hostname, username and
        password which can be used to run commands.
        """
        self._host = host
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            self._ssh.connect(hostname=host, username=username, password=password, timeout=60, look_for_keys=False)
        except paramiko.BadHostKeyException:
            raise SSHConnectionException('SSH Server host key could not be verified')
        except paramiko.AuthenticationException:
            raise SSHConnectionException('SSH Authentication failed')
        except paramiko.SSHException:
            raise SSHConnectionException('Paramiko SSH Connection Problem')
        except Exception as e:
            raise SSHConnectionException('SSH Connection Exception: {}'.format(e))

    def __repr__(self):
        """
        Return a representation string
        """
        return "<%s (%s)>" % (self.__class__.__name__, self._host)

    def __del__(self):
        """Try to close connection if possible"""
        try:
            sleep(2)
            self._ssh.close()
        except Exception:
            pass

    def _command(self, command):
        """
        Runs given command and returns output, error.
        This is the method you are after if none of the above fulfill your needs either to add more functionality or
        customize. You can run any command using SSH session established and parse the output the way you like.
        Example:
        def myfunc(ssh_session):
            output, error = ssh_session.command('date')
            return "".join(output).strip()
        """
        log.debug("Command being sent is " + command)
        try:
            stdin, stdout, stderr = self._ssh.exec_command(command)
            output = stdout.readlines()
            error = stderr.readlines()
            log.debug("Command output is")
            log.debug(output)
            log.debug("Command error is")
            log.debug(error)
            return output, error
        except Exception as e:
            raise SSHCommandException('Unable to run given command: {}. Exception: {}'.format(command, e))

    def _check_error(self, cmd, output):
        for eachout in output:
            eachout = eachout.strip().strip("\n")
            # print(eachout)
            if 'Syntax error' in eachout:
                return (True, eachout)
        return False, None

    def config(self, cmd):
        newcmd = "configure terminal ; " + cmd
        output, error = self._command(command=newcmd)
        flag, err = self._check_error(cmd, output)
        if flag:
            return output, err
        return output, None

    def show(self, cmd):
        newcmd = "end ; " + cmd
        output, error = self._command(command=newcmd)
        flag, err = self._check_error(cmd, output)
        if flag:
            return output, err
        return output, None
