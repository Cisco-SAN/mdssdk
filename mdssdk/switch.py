__author__ = "Suhas Bharadwaj (subharad)"

import logging
import re
import time
import os
import sys

from netmiko import CNTL_SHIFT_6
from .analytics import Analytics
from .constants import *
from .connection_manager.connect_netmiko import SSHSession
from .connection_manager.connect_nxapi import ConnectNxapi
from .connection_manager.errors import (
    CLIError,
    VersionNotFound,
    UnsupportedFeature,
    UnsupportedConfig,
)
from .constants import DEFAULT
from .nxapikeys import versionkeys, featurekeys
from .parsers.switch import ShowTopology
from .utility.switch_utility import SwitchUtils
from .utility import utils
from .utility.utils import get_key

log = logging.getLogger(__name__)

VALID_CONN_TYPES = ['https', 'https', 'ssh']

def print_and_log(msg):
    log.debug(msg)
    print(msg)


class Switch(SwitchUtils):
    """
    Switch module

    :param ip_address: mgmt ip address of switch
    :type ip_address: str
    :param username: username
    :type id: str
    :param password: password
    :type password: str
    :param connection_type: connection type 'http' or 'https'(optional, default: 'https')
    :type connection_type: str
    :param port: port number (optional, default: 8443 for https and 8080 for http)
    :type port: int
    :param timeout: timeout period in seconds (optional, default: 30)
    :type timeout: int
    :param verify_ssl: SSL verification (optional, default: True)
    :type verify_ssl: bool

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)

    """

    def __init__(
            self,
            ip_address,
            username,
            password,
            connection_type="https",
            port=None,
            timeout=NXAPI_CONN_TIMEOUT,
            verify_ssl=True,
    ):
        # Check if "NET_TEXTFSM" is set
        if "NET_TEXTFSM" not in os.environ:
            msg = "ERROR!! SDK is not installed correctly (NET_TEXTFSM is not set), please uninstall and follow the correct instructions from https://mdssdk.readthedocs.io/en/latest/readme.html#installation-steps"
            log.error(msg)
            sys.exit(msg)

        self.__ip_address = ip_address
        self.__username = username
        self.__password = password
        self.connection_type = connection_type
        if port is None:
            if connection_type == 'https':
                self.port = HTTPS_PORT
            elif connection_type == 'http':
                self.port = HTTP_PORT
        else:
            self.port = port
        self.timeout = timeout
        self.__verify_ssl = verify_ssl

        if self.connection_type != "ssh":
            log.info("Opening up a nxapi connection for switch with ip " + self.__ip_address)
            self.__connection = ConnectNxapi(
                host=self.__ip_address,
                username=self.__username,
                password=self.__password,
                transport=connection_type,
                port=self.port,
                verify_ssl=self.__verify_ssl,
            )
            log.info("Along with NXAPI opening up a parallel ssh connection for switch with ip " + self.__ip_address)
            self._set_connection_type_based_on_version()

        # Connect to ssh
        self._connect_to_ssh()
        log.debug("is_connection_type_ssh " + str(self.is_connection_type_ssh()))

    def _connect_to_ssh(self):
        log.debug("Opening up a ssh connection for switch with ip " + self.__ip_address)
        self._ssh_handle = SSHSession(
            host=self.__ip_address,
            username=self.__username,
            password=self.__password,
            timeout=self.timeout,
        )
        log.debug("Finished up a ssh connection for switch with ip " + self.__ip_address)
        self._SW_VER = self.version
        log.debug("sw version is " + self._SW_VER)

    def reconnect(self):
        self._reconnect_to_ssh()

    def _reconnect_to_ssh(self):
        log.debug("Re-establishing the ssh connection for switch with ip " + self.__ip_address)
        self._ssh_handle._reconnect()
        self._SW_VER = self.version
        log.debug("sw version is " + self._SW_VER)

    def _set_connection_type_based_on_version(self):
        log.info("Checking version on the switch with ip " + self.__ip_address)
        try:
            ver = self.version
            if ver is None:
                raise VersionNotFound("Unable to get the switch version, please check the log file")
            self._SW_VER = ver
            log.debug("sw version is " + self._SW_VER)
        except KeyError:
            log.error("Got keyerror while getting version, setting connection type to ssh. Please wait..")
            self.connection_type = "ssh"
            # Connect to ssh
            self._connect_to_ssh()
            ver = self._SW_VER
        PAT_VER = "(?P<major_plus>\d+)\.(?P<major>\d+)\((?P<minor>\d+)(?P<patch>[a-z+])?\)(?P<other>.*)"
        RE_COMP = re.compile(PAT_VER)
        result_ver = RE_COMP.match(ver)
        supported = "Ip: " + self.__ip_address + " Version: " + ver + ", it is 8.4(2a) or above. This is a supported version for using NXAPI"
        not_supported_str = "NOTE: Ip: " + self.__ip_address + " Version: " + ver + ", it is below 8.4(2a). This is NOT a supported version for using NXAPI, hence connection_type is set to 'ssh'"
        not_supported = utils.color.BOLD + utils.color.RED + not_supported_str + utils.color.END
        if result_ver:
            try:
                result_dict = result_ver.groupdict()
                majorplus = int(result_dict["major_plus"])
                major = int(result_dict["major"])
                minor = int(result_dict["minor"])
                patch = result_dict["patch"]
                other = result_dict["other"]
                if majorplus > 8:
                    log.info(supported)
                elif majorplus < 8:
                    log.warning(not_supported)
                    self.connection_type = "ssh"
                else:
                    if major > 4:
                        log.info(supported)
                    elif major < 4:
                        log.warning(not_supported)
                        self.connection_type = "ssh"
                    else:
                        if minor > 2:
                            log.info(supported)
                        elif minor < 2:
                            log.warning(not_supported)
                            self.connection_type = "ssh"
                        else:
                            if not patch:
                                log.warning(not_supported)
                                self.connection_type = "ssh"
                            else:
                                # it is 842a,842b etc..
                                log.info(supported)
            except Exception:
                log.error("Got execption while getting the switch version, setting connection type to ssh")
                self.connection_type = "ssh"
        else:
            log.error("Could not get the pattern match for version, setting connection type to ssh")
            self.connection_type = "ssh"

    def is_connection_type_ssh(self):
        return self.connection_type == "ssh"

    @property
    def ipaddr(self):
        """
        Get mgmt ip address of the switch

        :return: IP address of switch
        :rtype: str

        :example:
            >>> print(switch_obj.ipaddr)
            10.126.94.101
            >>>
        """

        return self.__ip_address

    @property
    def name(self):
        """
        get switchname or
        set switchname

        :getter:
        :return: switch name
        :rtype: str

        :example:
            >>> print(switch_obj.name)
            swTest
            >>>

        :setter:
        :param name: name of the switch that needs to be set
        :type name: str

        :example:
            >>> switch_obj.name = "yourswitchname"
            >>>

        .. warning:: Switch name must start with a letter, end with alphanumeric and contain alphanumeric and hyphen only. Max size 32.

        """

        return self.show(command="show switchname", raw_text=True).strip()

    @name.setter
    def name(self, swname):
        """

        :param swname:
        :return:
        """

        cmd = "switchname " + swname
        if self.is_connection_type_ssh():
            outlines, error = self._ssh_handle.config_change_switch_name(cmd)
            if error is not None:
                raise CLIError(cmd, error)
        else:
            self.config(cmd)

    @property
    def npv(self):
        """
        Check if switch is in NPV mode

        :return: Returns True if switch is in NPV, else returns False
        :rtype: bool

        :example:
            >>> print(switch_obj.npv)
            False
            >>>
        """
        # print("Getting npv")
        out = self.feature("npv")
        # print(out)
        return out

    @property
    def version(self):
        """
        Get the switch software version

        :return: version
        :rtype: str
        :raises CLIError: Raises if there was a command error or some generic error due to which version could not be fetched

        :example:
            >>> print(switch_obj.version)
            8.4(2)
            >>>
        """

        cmd = "show version"
        log.debug("Running version API")
        if self.is_connection_type_ssh():
            outlines = self.show(command=cmd)
            ver = outlines[0]["version"]
            log.debug("ssh: " + ver)
        else:
            out = self.show(command=cmd)
            if not out:
                raise CLIError(
                    cmd,
                    "Unable to fetch the switch software version using show version command. Need to debug further",
                )
            found = False
            allkeys = versionkeys.VER_STR.keys()
            for eachkey in allkeys:
                if eachkey in out.keys():
                    fullversion = out[versionkeys.VER_STR[eachkey]]
                    found = True
            if not found:
                fullversion = out[versionkeys.VER_STR[DEFAULT]]
            ver = fullversion.split()[0]
            log.debug("nxapi: " + ver)
        self._SW_VER = ver
        return ver

    @property
    def model(self):
        """
        Returns model of the switch

        :return: Returns model of the switch or returns None if model could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.model)
            MDS 9710 (10 Slot) Chassis
            >>>
            >>> print(switch2_obj.model)
            MDS 9396T 96X32G FC (2 RU) Chassis
            >>>
        """
        cmd = "show version"
        if self.is_connection_type_ssh():
            outlines = self.show(command=cmd)
            return outlines[0]["model"]
            # shver = ShowVersion(outlines)
            # return shver.model
        else:
            out = self.show(command=cmd)
            if not out:
                return None
            return out[get_key(versionkeys.CHASSIS_ID, self._SW_VER)]

    @property
    def form_factor(self):
        """
        Returns the form factor of the switch, i.e if its a 10 slot or 6 slot or 1RU or 2RU etc..

        :return: Returns form factor of the switch or returns None if form factor could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.form_factor)
            10 slot
            >>>
            >>> print(switch2_obj.form_factor)
            2 RU
            >>>
        """

        chassisid = self.model
        if chassisid is not None:
            pat = "MDS\s+(.*)\((.*)\)\s+Chassis"
            match = re.match(pat, chassisid)
            if match:
                ff = match.group(1).strip()
                type = match.group(2).strip()
                return ff
        return None

    @property
    def type(self):
        """
        Returns the type of the switch, i.e if its a 9710 or 9706 or 9396T etc..

        :return: Returns type of the switch or returns None if type could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.type)
            9710
            >>>
            >>> print(switch2_obj.type)
            9396T
            >>>

        """

        chassisid = self.model
        if chassisid is not None:
            pat = "MDS\s+(.*)\((.*)\)\s+Chassis"
            match = re.match(pat, chassisid)
            if match:
                ff = match.group(1).strip()
                type = match.group(2).strip()
                return type
        return None

    @property
    def image_string(self):
        """
        Returns the image's string that is specific to a particular platform example m9700-sf3ek9, m9100-s6ek9 etc..

        :return: Returns image string of the switch or returns None if image string could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.image_string)
            m9700-sf3ek9
            >>>
            >>> print(switch2_obj.image_string)
            m9300-s2ek9
            >>>

        """

        ff = self.form_factor.lower()
        if ff in ["9706", "9710", "9718"]:
            mods = self.modules
            for modnum, eachmod in mods.items():
                if "Supervisor Module-3" in eachmod.type:
                    return "m9700-sf3ek9"
                elif "Supervisor Module-4" in eachmod.type:
                    return "m9700-sf4ek9"
            return None
        elif "9132T".lower() in ff:
            return "m9100-s6ek9"
        elif "9148S".lower() in ff:
            return "m9100-s5ek9"
        elif "9148T".lower() in ff:
            return "m9148-s6ek9"
        elif "9250i".lower() in ff:
            return "m9250-s5ek9"
        elif "9396S".lower() in ff:
            return "m9300-s1ek9"
        elif "9396T".lower() in ff:
            return "m9300-s2ek9"
        elif "9148".lower() in ff:
            return "m9100-s3ek9"
        elif "9220i".lower() in ff:
            return "m9220-s7ek9"
        else:
            return None

    @property
    def kickstart_image(self):
        """
        Returns the kickstart image of the switch

        :return: Returns kickstart image of the switch or returns None if kickstart image could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.kickstart_image)
            bootflash:///m9700-sf3ek9-kickstart-mz.8.4.1.bin
            >>>
            >>> print(switch2_obj.kickstart_image)
            bootflash:///m9300-s2ek9-kickstart-mz.8.4.1.bin
            >>>
        """

        cmd = "show version"
        if self.is_connection_type_ssh():
            outlines = self.show(command=cmd)
            return outlines[0]["kickstart_image"]
            # shver = ShowVersion(outlines)
            # return shver.kickstart_image

        out = self.show(command=cmd)
        if not out:
            return None
        return out[get_key(versionkeys.KICK_FILE, self._SW_VER)]

    @property
    def system_image(self):
        """
        Returns the switch image of the switch

        :return: Returns switch image of the switch or returns None if switch image could not be fetched from the switch
        :rtype: str

        :example:
            >>> print(switch_obj.system_image)
            bootflash:///m9700-sf3ek9-mz.8.4.1.bin
            >>>
            >>> print(switch2_obj.system_image)
            bootflash:///m9300-s2ek9-mz.8.4.1.bin
            >>>
        """
        cmd = "show version"
        if self.is_connection_type_ssh():
            outlines = self.show(command=cmd)
            return outlines[0]["system_image"]
            # shver = ShowVersion(outlines)
            # return shver.system_image

        out = self.show(command=cmd)
        if not out:
            return None
        return out[get_key(versionkeys.ISAN_FILE, self._SW_VER)]

    @property
    def analytics(self):
        """
        Returns handler for analytics module, using which we could do analytics related operations

        :return: analytics handler
        :rtype: Analytics

        :example:
            >>> ana_handler = switch_obj.analytics
            >>>
        """

        return Analytics(self)

    # # Bug doesnt work on npv, NXOS needs to fix, once fixed uncomment this
    # def feature(self, name, enable=None):
    #
    #     """
    #     Enable or disable a feature or get the status of the feature
    #
    #     :param name: Name of the feature
    #     :param enable: Set to True to enable the feature or set to False to disable the feature or set to None (deafault) to get the status of the feature
    #     :return: Returns True of False if enable is set to None
    #
    #     :example:
    #         >>>
    #         >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
    #         >>> # Get the status of the feature, in this case analytics is disabled
    #         >>> ana = switch_obj.feature('analytics')
    #         >>> print(ana)
    #         False
    #         >>> # Now lets enable the feature
    #         >>> switch_obj.feature('analytics', True)
    #         >>> print(switch_obj.feature('analytics'))
    #         True
    #         >>> # Now lets disable the feature
    #         >>> switch_obj.feature('analytics', False)
    #         >>> print(switch_obj.feature('analytics'))
    #         False
    #         >>>
    #
    #     .. warning:: Disabling feature 'nxapi' or 'ssh' via this API is not allowed
    #
    #     """
    #     # Do a type check on the enable flag
    #     if enable is not None:
    #         if type(enable) is not bool:
    #             raise TypeError(
    #                 "enable flag must be True(to enable the feature) or False(to disable the feature)"
    #             )
    #
    #     if enable is None:
    #         log.debug("Get the status of the feature " + name)
    #         cmd = "show feature"
    #         out = self.show(command=cmd)
    #         # print(out)
    #
    #
    #         if self.is_connection_type_ssh():
    #             # print("--Get the status of the feature " + name)
    #             for eachrow in out:
    #                 if eachrow["feature"] == name:
    #                     if eachrow["state"] == "enabled":
    #                         return True
    #                     else:
    #                         return False
    #             return False
    #
    #         list_of_features = out["TABLE_cfcFeatureCtrl2Table"][
    #             "ROW_cfcFeatureCtrl2Table"
    #         ]
    #         for eachfeature in list_of_features:
    #             feature_name = eachfeature[
    #                 get_key(featurekeys.NAME, self._SW_VER)
    #             ].strip()
    #             feature_status = eachfeature[
    #                 get_key(featurekeys.STATUS, self._SW_VER)
    #             ].strip()
    #             if name == feature_name:
    #                 return feature_status == "enabled"
    #         return False
    #     elif enable:
    #         log.debug("Trying to enable the feature " + name)
    #         cmd = "feature " + name
    #     else:
    #         # if we try to disable ssh or nxapi via this SDK then throw an exception
    #         if name == "ssh" or name == "nxapi":
    #             raise UnsupportedConfig(
    #                 "Disabling the feature '"
    #                 + name
    #                 + "' via this SDK API is not allowed!!"
    #             )
    #         log.debug("Trying to disable the feature " + name)
    #         cmd = "no feature " + name
    #     try:
    #         out = self.config(cmd)
    #     except CLIError as c:
    #         if "Invalid command" in c.message:
    #             raise UnsupportedFeature(
    #                 "This feature '" + name + "' is not supported on this switch "
    #             )

    def feature(self, name, enable=None):

        """
        Enable or disable a feature or get the status of the feature

        :param name: Name of the feature
        :param enable: Set to True to enable the feature or set to False to disable the feature or set to None (deafault) to get the status of the feature
        :return: Returns True of False if enable is set to None

        :example:
            >>>
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
            >>> # Get the status of the feature, in this case analytics is disabled
            >>> ana = switch_obj.feature('analytics')
            >>> print(ana)
            False
            >>> # Now lets enable the feature
            >>> switch_obj.feature('analytics', True)
            >>> print(switch_obj.feature('analytics'))
            True
            >>> # Now lets disable the feature
            >>> switch_obj.feature('analytics', False)
            >>> print(switch_obj.feature('analytics'))
            False
            >>>

        .. warning:: Disabling feature 'nxapi' or 'ssh' via this API is not allowed

        """
        # Do a type check on the enable flag
        if enable is not None:
            if type(enable) is not bool:
                raise TypeError(
                    "enable flag must be True(to enable the feature) or False(to disable the feature)"
                )

        if enable is None:
            log.debug("Get the status of the feature " + name)
            cmd = "show feature"
            out = self.show(command=cmd, use_ssh=True)

            for eachrow in out:
                if eachrow["feature"] == name:
                    if eachrow["state"] == "enabled":
                        return True
                    else:
                        return False
            return False
        elif enable:
            log.debug("Trying to enable the feature " + name)
            cmd = "feature " + name
            if name == "npv":
                raise UnsupportedConfig(
                    "Enabling the feature '"
                    + name
                    + "' via this SDK API is not allowed!!"
                )
        else:
            # if we try to disable ssh or nxapi or npv via this SDK then throw an exception
            if name == "ssh" or name == "nxapi" or name == "npv":
                raise UnsupportedConfig(
                    "Disabling the feature '"
                    + name
                    + "' via this SDK API is not allowed!!"
                )
            log.debug("Trying to disable the feature " + name)
            cmd = "no feature " + name
        try:
            out = self.config(cmd, use_ssh=True)
        except CLIError as c:
            if "Invalid command" in c.message:
                raise UnsupportedFeature(
                    "This feature '" + name + "' is not supported on this switch "
                )

    @property
    def cores(self):
        """
        Check if any cores are present in the switch

        :return: list of cores present in the switch if any else None
        :rtype: list or None

        """

        out = self.show(command="show cores", use_ssh=True)
        log.debug(out)
        if type(out[0]) == str:
            return None
        return out

    def _cli_error_check(self, command_response):
        error = command_response.get(u"error")
        if error:
            command = command_response.get(u"command")
            if u"data" in error:
                raise CLIError(command, error[u"data"][u"msg"])
            else:
                raise CLIError(command, "Invalid command.")

        error = command_response.get(u"clierror")
        if error:
            command = command_response.get(u"input")
            raise CLIError(command, error)

    def _cli_command(self, commands, rpc=u"2.0", method=u"cli", timeout=CLI_CMD_TIMEOUT):
        if not isinstance(commands, list):
            commands = [commands]

        conn_response = self.__connection.send_request(
            commands, rpc_version=rpc, method=method, timeout=timeout
        )
        log.debug("conn_response is")
        log.debug(conn_response)

        text_response_list = []
        if rpc is not None:
            for command_response in conn_response:
                self._cli_error_check(command_response)
                text_response_list.append(command_response[u"result"])
        else:
            text_response_list = []
            for command_response in conn_response:
                if "ins_api" in command_response.keys():
                    retout = command_response["ins_api"]["outputs"]["output"]
                    if type(retout) is dict:
                        fullout = [retout]
                    else:
                        fullout = retout
                    for eachoutput in fullout:
                        # print(eachoutput)
                        self._cli_error_check(eachoutput)
                        text_response_list.append(eachoutput[u"body"])
                        # text_response_list.append(eachoutput)
        return text_response_list

    def _show_ssh(self, command, timeout, expect_string):
        log.debug(self.__ip_address + ":_show_ssh : Show cmd to be sent is " + " -- " + command)
        outlines, error = self._ssh_handle.show(command, timeout, expect_string)
        if error is not None:
            raise CLIError(command, error)
        return outlines

    def show(self, command, raw_text=False, use_ssh=False, expect_string=None, timeout=CLI_CMD_TIMEOUT):
        """
        Send a show command to the switch

        :param command: The command to send to the switch.
        :type command: str
        :param raw_text: If true then returns the command output in raw text(str) else it returns structured data(dict)
        :type raw_text: bool (default: False)
        :param use_ssh: If true then the cmd is sent over ssh channel
        :type use_ssh: bool (default: False)
        :param expect_string: string to expect after sending the show cmd, if set to None then it will expect the default string which is the cmd prompt
        :type expect_string: str (default: None)
        :param timeout: timeout for the show cmd sent
        :type timeout: int (default: 100)
        :raises CLIError: If there is a problem with the supplied command.
        :return: The output of the show command, which could be raw text(str) or structured data(dict).
        :rtype: dict
        """
        log.debug(self.__ip_address + ":Show cmd sent is " + " -- " + command)
        if self.is_connection_type_ssh() or use_ssh:
            if raw_text:
                textfsm = False
            else:
                textfsm = True
            outlines, error = self._ssh_handle.show(cmd=command, timeout=timeout, expect_string=expect_string,
                                                    use_textfsm=textfsm)
            # print("IN show")
            # print(error)
            # print(outlines)
            if error is not None:
                raise CLIError(command, error)
            if raw_text:
                log.debug("\n".join(outlines))
                return "\n".join(outlines)
            log.debug(self.__ip_address + ":Show cmd response is ")
            log.debug(outlines)
            return outlines
        else:
            commands = [command]
            list_result = self._show_list(commands, raw_text=raw_text, timeout=timeout)
            if list_result:
                log.debug(self.__ip_address + ":Show cmd response is ")
                log.debug(list_result[0])
                return list_result[0]
            else:
                log.debug(self.__ip_address + ":Show cmd response is ")
                log.debug("None or {}")
                return {}

    def _show_list(self, commands, raw_text=False, use_ssh=False, timeout=CLI_CMD_TIMEOUT):
        """
        Send a list of show commands to the switch

        :param commands: The list of commands to send to the switch.
        :type commands: list
        :param raw_text: If true then returns the command output in raw text(str) else it returns structured data(dict)
        :type raw_text: bool (default: False)
        :raises CLIError: If there is a problem with the supplied command.
        :return: The output of the show command, which could be raw text(str) or structured data(dict).
        :rtype: list
        """
        log.debug(self.__ip_address + ":Show cmds sent are " + " -- ".join(commands))
        if self.is_connection_type_ssh() or use_ssh:
            retdict = {}
            for cmd in commands:
                outlines, error = self._ssh_handle.show(cmd=cmd, timeout=timeout)
                if error is not None:
                    raise CLIError(cmd, error)
                # return outlines
                retdict[cmd] = outlines
            log.debug("Show commands sent over ssh are :")
            log.debug(commands)
            log.debug("Result got via ssh was :")
            log.debug(retdict)
            return retdict

        return_list = []
        if raw_text:
            response_list = self._cli_command(commands, method=u"cli_ascii", timeout=timeout)
            for response in response_list:
                if response:
                    return_list.append(response[u"msg"].strip())
        else:
            response_list = self._cli_command(commands, timeout=timeout)
            for response in response_list:
                if response:
                    return_list.append(response[u"body"])
                    # return_list.append(response)

        log.debug("Show commands sent over nxapi are :")
        log.debug(commands)
        log.debug("Result got via nxapi was :")
        log.debug(return_list)

        return return_list

    def config(self, command, rpc=u"2.0", method=u"cli", use_ssh=False, timeout=CLI_CMD_TIMEOUT):
        """
        Send any command to run from the config mode

        :param command: command to send to the switch
        :type command: str
        :raises CLIError: If there is a problem with the supplied command.
        :return: command output

        """
        log.debug(self.__ip_address + ":Config cmd sent is " + " -- " + command)
        if self.is_connection_type_ssh() or use_ssh:
            outlines, error = self._ssh_handle.config(command, timeout=timeout)
            if error is not None:
                raise CLIError(command, error)
            return outlines

        commands = [command]
        list_result = self._config_list(commands, rpc=rpc, method=method, timeout=timeout)
        if list_result[0] is not None:
            raise CLIError(command, list_result[0]["msg"])
        return list_result[0]

    def _config_list(self, commands, rpc=u"2.0", method=u"cli", use_ssh=False, timeout=CLI_CMD_TIMEOUT):
        """
        Send any list of commands to run from the config mode

        :param commands: list of commands to send to the switch
        :type command: list
        :raises CLIError: If there is a problem with the supplied command.
        :return: command output

        """
        log.debug(self.__ip_address + ":Config cmds sent are " + " -- ".join(commands))
        if self.is_connection_type_ssh() or use_ssh:
            retdict = {}
            for cmd in commands:
                outlines, error = self._ssh_handle.config(cmd, timeout=timeout)
                if error is not None:
                    raise CLIError(cmd, error)
                retdict[cmd] = outlines
            log.debug("Config commands sent via ssh are :")
            log.debug(commands)
            log.debug("Result got via ssh was :")
            log.debug(retdict)
            return retdict

        return_list = self._cli_command(commands, rpc=rpc, method=method, timeout=timeout)

        log.debug(self.__ip_address + ":Config commands sent via nxapi are :")
        log.debug(commands)
        log.debug(self.__ip_address + ":Result got via nxapi was :")
        log.debug(return_list)

        return return_list

    def reload(self, module=None, timeout=RELOAD_TIMEOUT, copyrs=True):
        """
        Reload a switch or a module

        :param module: if set to None reloads the switch else reloads the particular module
        :type module: int (default: None)
        :param timeout: time to wait for the switch/module to come up
        :type timeout: int (default: 300)
        :param copyrs: if set to True, executes copy r s before doing a reload
        :type copyrs: bool (default: True)
        :return: Returns {FAILED: <failed reason>} or {'SUCCESS': None}
        """
        if module is None:
            # Switch reload
            cmd = "terminal dont-ask ; reload"
            action_string = "reload switch"
            if copyrs:
                log.info("Reloading switch after copy running-config startup-config")
                crs = self.show(command="copy running-config startup-config", raw_text=True)
                if "Copy complete" in crs:
                    log.info("copy running-config startup-config is successful")
                else:
                    log.error("copy running-config startup-config failed")
                    log.error(crs.split("\n")[-1])
                    return {"FAILED": crs}
            else:
                log.info("Reloading switch without copy running-config startup-config")

        else:
            # Module reload
            mod = str(module)
            cmd = "terminal dont-ask ; reload module " + mod
            action_string = "reload module " + str(mod)
            if copyrs:
                log.info(
                    "Reloading the module "
                    + mod
                    + " after copy running-config startup-config"
                )
                crs = self.show(command="copy running-config startup-config", raw_text=True)
                if "Copy complete" in crs:
                    log.info("copy running-config startup-config is successful")
                else:
                    log.error("copy running-config startup-config failed")
                    log.error(crs.split("\n")[-1])
                    return {"FAILED": crs}
            else:
                log.info(
                    "Reloading the module "
                    + mod
                    + " without copy running-config startup-config"
                )

        out = self._verify_basic_stuff(cmd, action_string, timeout)
        return out

    def _get_alt_handle(self):
        log.debug("Getting an alt handle")
        alt_handle = SSHSession(
            host=self.__ip_address,
            username=self.__username,
            password=self.__password,
            timeout=self.timeout,
        )
        return alt_handle

    def issu(self, kickstart, system, timeout=ISSU_TIMEOUT, expect_string=r".*"):
        self.curr_status = None
        cmd = (
                "terminal dont-ask ; install all kickstart "
                + kickstart
                + " system "
                + system
        )
        self.show(command=cmd, expect_string=expect_string, timeout=timeout)
        return True

    def get_install_all_status(self):
        # Flags and status init
        sys.tracebacklimit = 0
        # sys.excepthook = self._exceptionHandler
        if self.curr_status is None:
            self.curr_status = "Install in progress"
        try:
            alt_handle = self._get_alt_handle()
            self._reconnect_to_ssh()

            log.debug(self.ipaddr + " Sending the cmd show install all status")
            cmd = "show install all status"
            # alt_handle._connection.write_channel("\nend\n")
            # out = alt_handle._connection.read_channel()
            # log.debug(out)
            alt_handle._connection.write_channel(cmd + "\n")
            time.sleep(0.1)
            alt_handle._connection.write_channel(CNTL_SHIFT_6)
            time.sleep(0.5)
            out = alt_handle._connection.read_channel()
            log.debug(out)
            status = alt_handle._connection.normalize_linefeeds(alt_handle._connection.strip_prompt(out)).split("\n")
            log.debug(self.ipaddr + " read channel o/p")
            while "" in status:
                status.remove("")
            status.reverse()
            log.debug(status)
            if status:
                temp = ""
                for eachline in status:
                    if "Install has been successful" in eachline:
                        self.curr_status = "Install has been successful"
                        break
                    elif "Non-disruptive upgrading" in eachline:
                        temp = eachline
                        continue
                    elif "Module" in eachline and "<" in eachline:  # Module 2: <Mon Sep 14 12:50:06>
                        z = eachline.split("<")[0].strip() + temp
                        self.curr_status = z[:60]
                        break
                    elif "<" in eachline:  # SUCCESS <Tue Sep 15 13:33:38>
                        continue
                    elif "#" in eachline:
                        continue
                    elif "(" in eachline:  # 2      slcf32                                   8.4(2a)               8.4(2b)
                        continue
                    elif "Module" in eachline:  # Module       Image
                        continue
                    elif "--" in eachline:  # ------  ----------
                        continue
                    elif "^" in eachline:  # for ctrl C
                        continue
                    elif "yes" in eachline:
                        continue
                    elif "hitless" in eachline:  # FC ports 1-24 are hitless,
                        continue
                    elif cmd in eachline:
                        continue
                    else:
                        self.curr_status = eachline.strip()[:60]
                        break
            log.debug("Deleting alt handle")
            del (alt_handle)
        except Exception as e:
            log.debug("Exception in get_install_status")
            self.curr_status = "Switch is going for reboot/switchover as part of install"
            log.debug(self.curr_status)
            # log.debug(e, exc_info=True)
            sys.tracebacklimit = 1
            return self.curr_status
        sys.tracebacklimit = 1
        return self.curr_status

    def discover_peer_npv_switches(self):
        if self.npv:
            log.error("This is an NPV switch, cannot discover peer switches using NPV switch")
            return None
        peer_ip_list = utils._run_show_fcns_for_npv(self)
        return list(set(peer_ip_list))

    def discover_peer_switches(self):
        """
        :return: list of switch ips discovered
        """
        if self.npv:
            log.error("This is an NPV switch, cannot discover peer switches using NPV switch")
            return None
        peer_ip_list = utils._run_show_topo_for_npiv(self)
        return list(set(peer_ip_list))

