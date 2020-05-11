__author__ = 'Suhas Bharadwaj (subharad)'

import logging
import re

import requests
import time

from .analytics import Analytics
from .connection_manager.connect_netmiko import SSHSession
from .connection_manager.connect_nxapi import ConnectNxapi
from .connection_manager.errors import CLIError, CustomException
from .constants import DEFAULT
from .nxapikeys import versionkeys, featurekeys
from .parsers.switch import ShowVersion, ShowFeature, ShowTopology
from .utility.switch_utility import SwitchUtils
from .utility.utils import get_key

log = logging.getLogger(__name__)


class UnsupportedVersion(CustomException):
    pass


class VersionNotFound(CustomException):
    pass


class UnsupportedFeature(CustomException):
    pass


class UnsupportedConfig(CustomException):
    pass


def log_exception(logger):
    # A decorator that wraps the passed in function and logs
    # exceptions should one occur

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
            # re-raise the exception
            raise

        return wrapper

    return decorator


def print_and_log(msg):
    log.info(msg)
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
    :param port: port number (optional, default: 8443)
    :type port: int
    :param timeout: timeout period in seconds (optional, default: 30)
    :type timeout: int
    :param verify_ssl: SSL verification (optional, default: True)
    :type verify_ssl: bool

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)

    """

    def __init__(self, ip_address, username, password, connection_type='https', port=8443, timeout=30, verify_ssl=True):

        self.__ip_address = ip_address
        self.__username = username
        # self.__password = password
        self.connection_type = connection_type
        self.port = port
        self.timeout = timeout
        self.__verify_ssl = verify_ssl

        if self.connection_type != 'ssh':
            log.info("Opening up a connection for switch with ip " + ip_address)
            self.__connection = ConnectNxapi(ip_address, username, password, transport=connection_type, port=port,
                                             verify_ssl=verify_ssl)

        self._ssh_handle = SSHSession(host=ip_address, username=username, password=password, timeout=timeout)
        self.can_connect = False
        # Get version of the switch and log it
        # self._log_version()

        # Verify that version is 8.4(2) and above
        # self._verify_supported_version()

        self._set_connection_type_based_on_version()

    def _set_connection_type_based_on_version(self):
        try:
            ver = self.version
            if ver is None:
                raise VersionNotFound("Unable to get the switch version, please check the log file")
        except KeyError:
            log.debug("Got keyerror while getting version, setting connection type to ssh")
            self.connection_type = "ssh"
        PAT_VER = "(?P<major_plus>\d+)\.(?P<major>\d+)\((?P<minor>\d+)(?P<patch>.*)\)"
        RE_COMP = re.compile(PAT_VER)
        result_ver = RE_COMP.match(ver)
        if result_ver:
            try:
                result_dict = result_ver.groupdict()
                majorplus = int(result_dict['major_plus'])
                major = int(result_dict['major'])
                minor = int(result_dict['minor'])
                patch = result_dict['patch']
                if majorplus >= 8 and major >= 4 and minor >= 2:
                    log.debug("Switch version is " + ver + ". This is a supported switch version for using NXAPI")
                else:
                    log.debug("Switch version is not 8.4(2), setting connection type to ssh")
                    self.connection_type = "ssh"
            except Exception:
                log.debug("Got execption while getting the switch version, setting connection type to ssh")
                self.connection_type = "ssh"
        else:
            log.debug("Could not get the pattern match for version, setting connection type to ssh")
            self.connection_type = "ssh"

    def _verify_supported_version(self):
        ver = self.version
        PAT_VER = "(?P<major_plus>\d+)\.(?P<major>\d+)\((?P<minor>\d+)(?P<patch>.*)\)"
        RE_COMP = re.compile(PAT_VER)
        result_ver = RE_COMP.match(ver)
        if result_ver:
            try:
                result_dict = result_ver.groupdict()
                majorplus = int(result_dict['major_plus'])
                major = int(result_dict['major'])
                minor = int(result_dict['minor'])
                patch = result_dict['patch']
                if majorplus >= 8 and major >= 4 and minor >= 2:
                    log.debug("Switch version is " + ver + ". This is a supported switch version for SDK")
                else:
                    raise UnsupportedVersion(
                        "Switch version: " + ver + "\n SDK does not support this switch version. Supported version are 8.4(2) and above")
            except KeyError:
                raise UnsupportedVersion(
                    "Switch version: " + ver + "\n SDK does not support this switch version. Supported version are 8.4(2) and above")
            except ValueError:
                raise UnsupportedVersion(
                    "Switch version: " + ver + "\n SDK does not support this switch version. Supported version are 8.4(2) and above")
        else:
            raise UnsupportedVersion(
                "Switch version: " + ver + "\n SDK does not support this switch version. Supported version are 8.4(2) and above")

    def is_connection_type_ssh(self):
        return self.connection_type == 'ssh'

    @log_exception(log)
    def _log_version(self):
        """

        :return:
        """
        try:
            log.debug(self.version)
            self.can_connect = True
        except requests.exceptions.ConnectionError as e:
            msg = "ERROR!! Unable to get the switch version or may be connection refused for the switch : " + self.ipaddr + \
                  " Verify that the switch has " + self.connection_type + " configured with port " + str(self.port)
            log.error(msg)

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

        return self.show("show switchname", raw_text=True).strip()

    @name.setter
    def name(self, swname):
        """

        :param swname:
        :return:
        """
        self.config("switchname " + swname)

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
        return self.feature("npv")
        # return self.__is_npv_switch()

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

        if self.is_connection_type_ssh():
            outlines = self.show(cmd)
            shver = ShowVersion(outlines)
            ver = shver.version
        else:
            out = self.show(cmd)
            if not out:
                raise CLIError(cmd,
                               'Unable to fetch the switch software version using show version command. Need to debug further')
            found = False
            allkeys = versionkeys.VER_STR.keys()
            for eachkey in allkeys:
                if eachkey in out.keys():
                    fullversion = out[versionkeys.VER_STR[eachkey]]
                    found = True
            if not found:
                fullversion = out[versionkeys.VER_STR[DEFAULT]]
            ver = fullversion.split()[0]
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
            outlines = self.show(cmd)
            shver = ShowVersion(outlines)
            return shver.model
        out = self.show(cmd)
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

        ff = self.form_factor
        if ff in ["9706", "9710", "9718"]:
            mods = self.modules
            for eachmod in mods:
                if "Supervisor Module-3" in eachmod.module_type:
                    return "m9700-sf3ek9"
                elif "Supervisor Module-4" in eachmod.module_type:
                    return "m9700-sf4ek9"
            return None
        elif "9132T" in ff:
            return "m9100-s6ek9"
        elif "9148S" in ff:
            return "m9100-s5ek9"
        elif "9148T" in ff:
            return "m9148-s6ek9"
        elif "9250i" in ff:
            return "m9250-s5ek9"
        elif "9396S" in ff:
            return "m9300-s1ek9"
        elif "9396T" in ff:
            return "m9300-s2ek9"
        elif "9148" in ff:
            return "m9100-s3ek9"
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
            outlines = self.show(cmd)

            shver = ShowVersion(outlines)
            return shver.kickstart_image

        out = self.show(cmd)
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
            outlines = self.show(cmd)
            shver = ShowVersion(outlines)
            return shver.system_image

        out = self.show(cmd)
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
                raise TypeError("enable flag must be True(to enable the feature) or False(to disable the feature)")

        if enable is None:
            log.debug("Get the status of the feature " + name)
            cmd = "show feature"
            out = self.show(cmd)

            if self.is_connection_type_ssh():
                shfea = ShowFeature(out)
                return shfea.is_enabled(name)

            list_of_features = out['TABLE_cfcFeatureCtrl2Table']['ROW_cfcFeatureCtrl2Table']
            for eachfeature in list_of_features:
                feature_name = eachfeature[get_key(featurekeys.NAME, self._SW_VER)].strip()
                feature_status = eachfeature[get_key(featurekeys.STATUS, self._SW_VER)].strip()
                if name == feature_name:
                    return feature_status == 'enabled'
            return False
        elif enable:
            log.debug("Trying to enable the feature " + name)
            cmd = "feature " + name
            try:
                self.config(cmd)
            except CLIError as c:
                if "Invalid command" in c.message:
                    raise UnsupportedFeature("This feature '" + name + "' is not supported on this switch ")
        else:
            # if we try to disable ssh or nxapi via this SDK then throw an exception
            if name == 'ssh' or name == 'nxapi':
                raise UnsupportedConfig("Disabling the feature '" + name + "' via this SDK API is not allowed!!")
            log.debug("Trying to disable the feature " + name)
            cmd = "no feature " + name
            self.config(cmd)

    @property
    def cores(self):
        """
        Check if any cores are present in the switch

        :return: list of cores present in the switch if any else None
        :rtype: list or None

        """
        retval = []
        PAT = "(?P<module>\d+)\s+(?P<instance>\d+)\s+(?P<process_name>\S+)\s+(?P<pid>\d+)\s+(?P<date_time>.*)"
        PAT_COMP = re.compile(PAT)
        cmd = "show cores"
        out = self.show(cmd, raw_text=True)
        alllines = out.splitlines()
        for line in alllines:
            result = PAT_COMP.match(line)
            if result:
                d = result.groupdict()
                retval.append(d)
        if retval:
            return retval

    def _cli_error_check(self, command_response):
        error = command_response.get(u'error')
        if error:
            command = command_response.get(u'command')
            if u'data' in error:
                raise CLIError(command, error[u'data'][u'msg'])
            else:
                raise CLIError(command, 'Invalid command.')

        error = command_response.get(u'clierror')
        if error:
            command = command_response.get(u'input')
            raise CLIError(command, error)

    def _cli_command(self, commands, rpc=u'2.0', method=u'cli'):
        if not isinstance(commands, list):
            commands = [commands]

        conn_response = self.__connection.send_request(commands, rpc_version=rpc, method=method, timeout=self.timeout)
        log.debug("conn_response is")
        log.debug(conn_response)

        text_response_list = []
        if rpc is not None:
            for command_response in conn_response:
                self._cli_error_check(command_response)
                text_response_list.append(command_response[u'result'])
        else:
            text_response_list = []
            for command_response in conn_response:
                if 'ins_api' in command_response.keys():
                    retout = command_response['ins_api']['outputs']['output']
                    if type(retout) is dict:
                        fullout = [retout]
                    else:
                        fullout = retout
                    for eachoutput in fullout:
                        # print(eachoutput)
                        self._cli_error_check(eachoutput)
                        text_response_list.append(eachoutput[u'body'])
        return text_response_list

    def show(self, command, raw_text=False, use_ssh=False):
        """
        Send a show command to the switch

        :param command: The command to send to the switch.
        :type command: str
        :param raw_text: If true then returns the command output in raw text(str) else it returns structured data(dict)
        :type raw_text: bool (default: False)
        :raises CLIError: If there is a problem with the supplied command.
        :return: The output of the show command, which could be raw text(str) or structured data(dict).
        :rtype: dict
        """
        log.debug("Show cmd to be sent is " + ' -- ' + command)
        if self.is_connection_type_ssh() or use_ssh:
            outlines, error = self._ssh_handle.show(command)
            if error is not None:
                raise CLIError(command, error)
            return outlines

        commands = [command]
        list_result = self.show_list(commands, raw_text)
        if list_result:
            return list_result[0]
        else:
            return {}

    def show_list(self, commands, raw_text=False, use_ssh=False):
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
        log.debug("Show cmds to be sent are " + ' -- '.join(commands))
        if self.is_connection_type_ssh() or use_ssh:
            retdict = {}
            for cmd in commands:
                outlines, error = self._ssh_handle.show(cmd)
                if error is not None:
                    raise CLIError(command, error)
                return outlines
                retdict[cmd] = outlines
            log.debug("Show commands sent are :")
            log.debug(commands)
            log.debug("Result got via ssh was :")
            log.debug(retdict)
            return retdict

        return_list = []
        if raw_text:
            response_list = self._cli_command(commands, method=u'cli_ascii')
            for response in response_list:
                if response:
                    return_list.append(response[u'msg'].strip())
        else:
            response_list = self._cli_command(commands)
            for response in response_list:
                if response:
                    return_list.append(response[u'body'])

        log.debug("Show commands sent are :")
        log.debug(commands)
        log.debug("Result got was :")
        log.debug(return_list)

        return return_list

    def config(self, command, rpc=u'2.0', method=u'cli', use_ssh=False):
        """
        Send any command to run from the config mode

        :param command: command to send to the switch
        :type command: str
        :raises CLIError: If there is a problem with the supplied command.
        :return: command output

        """
        log.debug("Config cmd to be sent is " + ' -- ' + command)
        if self.is_connection_type_ssh() or use_ssh:
            outlines, error = self._ssh_handle.config(command)
            if error is not None:
                # raise Exception(command, error)
                raise CLIError(command, error)
            return outlines

        commands = [command]
        list_result = self.config_list(commands, rpc, method)
        return list_result[0]

    def config_list(self, commands, rpc=u'2.0', method=u'cli'):
        """
        Send any list of commands to run from the config mode

        :param commands: list of commands to send to the switch
        :type command: list
        :raises CLIError: If there is a problem with the supplied command.
        :return: command output

        """
        log.debug("Show cmds to be sent are " + ' -- '.join(commands))
        return_list = self._cli_command(commands, rpc=rpc, method=method)

        log.debug("Config commands sent are :")
        log.debug(commands)
        log.debug("Result got was :")
        log.debug(return_list)

        return return_list

    def reload(self, module=None, timeout=300, copyrs=True):
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
                crs = self.show("copy running-config startup-config", raw_text=True)
                if 'Copy complete' in crs:
                    log.info('copy running-config startup-config is successful')
                else:
                    log.error('copy running-config startup-config failed')
                    log.error(crs.split("\n")[-1])
                    return {'FAILED': crs}
            else:
                log.info("Reloading switch without copy running-config startup-config")

        else:
            # Module reload
            mod = str(module)
            cmd = "terminal dont-ask ; reload module " + mod
            action_string = "reload module " + str(mod)
            if copyrs:
                log.info("Reloading the module " + mod + " after copy running-config startup-config")
                crs = self.show("copy running-config startup-config", raw_text=True)
                if 'Copy complete' in crs:
                    log.info('copy running-config startup-config is successful')
                else:
                    log.error('copy running-config startup-config failed')
                    log.error(crs.split("\n")[-1])
                    return {'FAILED': crs}
            else:
                log.info("Reloading the module " + mod + " without copy running-config startup-config")

        out = self._verify_basic_stuff(cmd, action_string, timeout)
        return out

    def issu(self, kickstart, system, timeout=600, post_issu_checks=True):
        print_and_log("Doing basic checks before starting ISSU")
        # Set the switch timeout
        if timeout < 600:
            log.info("Timeout for ISSU cannot be less than 10 mins (600 sec)")
            timeout = 600
        self.timeout = timeout

        # Check if any compatibilty issues
        # show incompatibility-all system bootflash:/m9700-sf4ek9-mz.8.4.1.bin
        cmd = "show incompatibility-all system " + system
        out = self.show(cmd, raw_text=True)
        alllines = out.splitlines()
        noincompat = 0
        for eachline in alllines:
            if "No incompatible configurations" in eachline:
                noincompat += 1
        if noincompat != 2:
            log.error("Incompatibilty check failed, please fix the incompatibilities")
            log.error(out)
            return {'FAILED': out}
        print_and_log("There are no incompatible configurations so continuing with ISSU checks")

        # Check impact status to determine if its disruptive or non-disruptive
        # show install all impact kickstart m9700-sf4ek9-kickstart-mz.8.4.1.bin system m9700-sf4ek9-mz.8.4.1.bin
        cmd = "show install all impact kickstart " + kickstart + " system " + system
        out = self.show(cmd, raw_text=True)
        alllines = out.splitlines()
        nondisruptive = False
        for eachline in alllines:
            if "non-disruptive" in eachline:
                nondisruptive = True
                print_and_log("'show install all impact' was success, continuing with non-disruptive ISSU ")
                break
        if not nondisruptive:
            log.error("Cannot do non-disruptive upgrade")
            log.error(out)
            return {'FAILED': out}

        cmd = "terminal dont-ask ; install all kickstart " + kickstart + " switch " + system
        if post_issu_checks:
            out = self._verify_basic_stuff(cmd, "install all", timeout)
        else:
            out = self._execute_install_all(cmd, timeout)
        return out

    def _execute_install_all(self, cmd, timeout):
        # Send install all cmd
        try:
            out = self.config(cmd)
        except CLIError as e:
            if "Installer will perform compatibility check first. Please wait" not in e.message:
                raise CLIError

        # Wait for install all to start
        print_and_log("Sent install command. Please wait for install all to complete. This will take a while...")
        time.sleep(1800)

        # Wait for atleast half hr
        # Wait every 5 mins and check if install is a success
        if timeout < 1800:
            waittime = 1800
        else:
            waittime = timeout

        timestocheck = int(waittime / 300)

        for i in range(timestocheck):
            print_and_log("Checking if install is complete and successful. Please wait...")

            # show install all status - Install has been successful
            cmd = "show install all status"
            out = self.show(cmd, raw_text=True)
            log.debug(out)
            alllines = out.splitlines()
            for eachline in alllines:
                if "Install has been successful" in eachline:
                    print_and_log("Install has been successful")
                    return ('SUCCESS', None)
            time.sleep(300)

        log.error(
            "Could not get install all success message from show install all status cmd, please check the log file for more details")
        log.info(out)
        return ('FAILED', out)

    def _verify_basic_stuff(self, cmd, action_string, timeout):
        shmod_before = self.show("show module", raw_text=True).split("\n")
        shintb_before = self.show("show interface brief", raw_text=True).split("\n")
        print_and_log("Doing " + action_string + " . Please wait...")
        if "install all" in action_string:
            status, error = self._execute_install_all(cmd, timeout)
            if status == "FAILED":
                return status, error
        else:
            out = self.config(cmd)
            print_and_log("Please wait for " + str(timeout) + "secs..")
            time.sleep(timeout)
        shmod_after = self.show("show module", raw_text=True).split("\n")
        shintb_after = self.show("show interface brief", raw_text=True).split("\n")

        cores = self.cores
        if cores is not None:
            log.error(
                "Cores present on the switch, please check the switch and also the log file")
            log.error(cores)
            return {'FAILED': out}

        if shmod_before == shmod_after:
            log.info("'show module' is correct after " + action_string)
        else:
            log.error(
                "'show module' output is different from before and after " + action_string + ", please check the log file")
            log.debug("'show module' before " + action_string)
            log.debug(shmod_before)
            log.debug("'show module' after " + action_string)
            log.debug(shmod_after)

            bset = set(shmod_before)
            aset = set(shmod_after)
            bef = list(bset - aset)
            aft = list(aset - bset)
            log.debug("diff of before after " + action_string)
            log.debug(bef)
            log.debug(aft)
            return {'FAILED': [bef, aft]}

        if shintb_before == shintb_after:
            log.info("'show interface brief' is correct after " + action_string)
        else:
            log.error(
                "'show interface brief' output is different from before and after " + action_string + ", please check the log file")
            log.debug("'show interface brief' before " + action_string)
            log.debug(shintb_before)
            log.debug("'show interface brief' after " + action_string)
            log.debug(shintb_after)

            bset = set(shintb_before)
            aset = set(shintb_after)
            bef = list(bset - aset)
            aft = list(aset - bset)
            log.debug("diff of before after " + action_string)
            log.debug(bef)
            log.debug(aft)
            return {'FAILED': [bef, aft]}
        return {'SUCCESS': None}

    def get_peer_switches(self):
        peer_sw_list = []
        shtopoout = self.show("show topology", raw_text=True)
        sh = ShowTopology(shtopoout.splitlines())
        for vsan, interfacelist in sh.parse_data.items():
            for eachinterface in interfacelist:
                peer_sw_ip = eachinterface['peer_ip']
                peer_sw_list.append(peer_sw_ip)
        peerlist = list(dict.fromkeys(peer_sw_list))
        log.debug("Peer NPIV list of switch : " + self.ipaddr + " are: ")
        log.debug(peerlist)
        return peerlist

    def get_peer_npv_switches(self):
        retout = []
        try:
            fcnsout = self.show("show fcns database detail")['TABLE_fcns_vsan']['ROW_fcns_vsan']
        except KeyError:
            return None
        if type(fcnsout) is dict:
            fcnsout = [fcnsout]
        for eachline in fcnsout:
            temp = eachline['TABLE_fcns_database']['ROW_fcns_database']
            # print(temp)
            if type(temp['fc4_types_fc4_features']) is str:
                if temp['fc4_types_fc4_features'].strip() == 'npv':
                    ip = temp['node_ip_addr']
                    retout.append(ip)
        peerlist = list(dict.fromkeys(retout))
        log.debug("Peer NPV list of switch : " + self.ipaddr + " are: ")
        log.debug(peerlist)
        return peerlist
