import logging
import re
from time import sleep

from netmiko import ConnectHandler

log = logging.getLogger(__name__)


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
        self._cisco_device = {
            "device_type": "cisco_nxos",
            "host": self._host,
            "username": username,
            "password": password,
            "timeout": 60,
        }
        self.anyerror = False
        self._connect()

    def __repr__(self):
        """
        Return a representation string
        """
        return "<%s (%s)>" % (self.__class__.__name__, self._host)

    def __del__(self):
        """Try to close connection if possible"""
        try:
            sleep(2)
            self._disconnect()
        except Exception:
            pass

    def _reconnect(self):
        log.debug("Inside reconnect " + self._host)
        self._disconnect()
        self._connect()

    def _disconnect(self):
        if not self.anyerror:
            log.debug("Inside disconnect " + self._host)
            self._connection.disconnect()

    def _connect(self):
        log.debug("Inside Connect " + self._host)
        self._connection = ConnectHandler(**self._cisco_device)
        self.prompt = self._connection.find_prompt()
        log.debug("Prompt is " + self.prompt)

    def _check_error(self, output):
        for eachline in output.strip().splitlines():
            eachline = eachline.strip()
            eachline = eachline.replace("at '^' marker.", "")
            eachline = eachline.replace("^", "")
            if "Invalid command" in eachline:
                return True
            if "Invalid range" in eachline:
                return True
        return False

    def show(self, cmd, timeout=100, expect_string=None, use_textfsm=True):
        df = int(timeout / 100)
        output = self._connection.send_command(
            cmd,
            delay_factor=df,
            expect_string=expect_string,
            use_textfsm=use_textfsm,
            strip_prompt=True,
        )
        if type(output) == str:
            # Output did not go through textFSM, as maybe there was no template
            if self._check_error(output):
                return output.splitlines(), output  # There is error - invalid command
            return output.splitlines(), None  # There is no error
        else:
            # Output did go through textFSM, as maybe there was no template
            return output, None

    def config_change_switch_name(self, cmd):
        cmd = "configure terminal ; " + cmd + " ; end"
        out, err = self.show(cmd, expect_string="#")
        # Need to reconnect to get the prompt to reset
        self._reconnect()
        retout = []
        for eachline in out:
            eachline = eachline.strip()
            eachline = eachline.replace("at '^' marker.", "")
            eachline = eachline.replace("^", "")
            if "Enter configuration commands, one per line" in eachline:
                continue
            if re.match(r"^\s*$", eachline):
                continue
            if self.prompt in eachline:
                continue
            if re.match(r"^.*$", eachline):
                retout.append(eachline)
        if retout:
            return retout, " ".join(retout)  # There is some error
        return retout, None  # there is no error

    def config(self, cmd):
        retout = []
        output = self._connection.send_config_set(
            cmd,
            strip_prompt=True,
            strip_command=True,
            config_mode_command="configure terminal",
            exit_config_mode=True,
        )
        start = False
        for eachline in output.strip().splitlines():
            eachline = eachline.strip()
            eachline = eachline.replace("at '^' marker.", "")
            eachline = eachline.replace("^", "")
            if re.match(r"^\s*$", eachline):
                continue
            if cmd.strip() in eachline:
                start = True
                continue
            if "# end" in eachline:
                break
            if start:
                retout.append(eachline)
        if retout:
            return retout, " ".join(retout)  # There is some error
        return retout, None  # there is no error
