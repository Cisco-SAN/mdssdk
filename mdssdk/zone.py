import logging
import re

import time

from .connection_manager.errors import (
    CLIError,
    InvalidZoneMode,
    InvalidDefaultZone,
    InvalidZoneMemberType,
    UnsupportedSwitch,
)
from .constants import ENHANCED, BASIC, PERMIT, DENY, PAT_WWN, VALID_PIDS_MDS
from .fc import Fc
from .nxapikeys import zonekeys
from .portchannel import PortChannel
from .utility.utils import get_key
from .vsan import Vsan

log = logging.getLogger(__name__)


class Zone(object):
    """
    Zone module

    :param switch: switch object on which zone operations needs to be executed
    :type switch: Switch
    :param name: zone name with which zone operations needs to be executed
    :type name: str
    :param vsan: vsan id on which zone operations needs to be executed
    :type vsan: int
    :raises CLIError: if vsan is not present on the switch
    :example:
        >>>
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
        >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
        >>>
    """

    def __init__(self, switch, name, vsan, check_npv=True):
        self.__swobj = switch
        self._SW_VER = switch._SW_VER
        self._vsan = vsan
        self._name = name
        self.__zones = None
        self.__rpc = None
        self.__method = u"cli_conf"
        self._part_of_active_zs = False
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )
        if check_npv:
            self._check_if_npv()

    # Make sure that the switch is not in NPV mode
    def _check_if_npv(self):
        if self.__swobj.npv:
            raise TypeError(
                "Switch("
                + self.__swobj.ipaddr
                + ") is in NPV mode, hence cannot create zone/zoneset object"
            )

    def _set_part_of_active(self, val):
        self._part_of_active_zs = val

    @property
    def name(self):
        """
        Get zone name

        :return: name: Zone name
        :rtype: str
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> zoneObj.create()
            >>> print(zoneObj.name)
            zone_fab_a
            >>>
        """
        out = self.__show_zone_name()
        if out:
            if self.__swobj.is_connection_type_ssh():
                return out[0]["zone_name"]
            else:
                return out[get_key(zonekeys.NAME, self._SW_VER)]
        return None

    @property
    def vsan(self):
        """
        Get vsan object for the zone

        :return: vsan: vsan of the zone
        :rtype: Vsan
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> print(zoneObj.vsan)
            <mdslib.vsan.Vsan object at 0x10d105550>
            >>> print(zoneObj.vsan.id)
            2
            >>>

        """
        vsan_obj = Vsan(switch=self.__swobj, id=self._vsan)
        return vsan_obj

    @property
    def members(self):
        """
        Get members of the zone

        :return: members: members of the zone
        :rtype: list
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.members)
            [{'interface': 'fc1/2'}, {'interface': 'fc1/3'}, {'device-alias': 'somename'}, {'pwwn': '11:22:33:44:55:66:77:88'}]
            >>>

        """
        retout = []
        out = self.__show_zone_name()
        if out:
            if self.__swobj.is_connection_type_ssh():
                retout = self.__format_members_ssh(out)
            else:
                try:
                    retout = out["TABLE_zone_member"]["ROW_zone_member"]
                except KeyError:
                    return retout
                if type(retout) is dict:
                    # means there is only one member for the zone, so convert to list and return
                    # return self.__format_members([retout])
                    retout = [retout]
        return retout

    @property
    def active_members(self):
        """
        Get active members of the zone i.e zone members part of active zoneset

        :return: members: active members of the zone i.e zone members part of active zoneset
        :rtype: list
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.active_members)
            [{'interface': 'fc1/2'}, {'interface': 'fc1/3'}, {'device-alias': 'somename'}, {'pwwn': '11:22:33:44:55:66:77:88'}]
            >>>

        """
        retout = []
        out = self.__show_zone_name_active()
        if out:
            if self.__swobj.is_connection_type_ssh():
                retout = self.__format_members_ssh_active(out)
            else:
                try:
                    out = out["TABLE_zone_member"]["ROW_zone_member"]
                    if type(out) is dict:
                        # means there is only one member for the zone, so convert to list
                        out = [out]
                    retout = self.__format_members_nxapi(out)
                except KeyError:
                    return retout
        return retout

    def __format_members_nxapi(self, out):
        log.debug("Before __format_members_nxapi")
        log.debug(out)
        retout = []
        for eachmem in out:
            mem_dict = {}
            for k, v in eachmem.items():
                if k == "online_fcid" and v == "":
                    break
                else:
                    mem_dict[k] = v
            if mem_dict:
                retout.append(mem_dict)
        log.debug("After __format_members_nxapi")
        log.debug(retout)
        return retout

    def __format_members_ssh(self, out):
        # SSH o/p via textfsm template
        log.debug("Before __format_members_ssh")
        log.debug(out)
        retout = []
        for eachmem in out:
            mem_dict = {}
            for k, v in eachmem.items():
                if k == "type" and v == "":
                    break
                elif k == "vsan" or k == "zone_name" or v == "":
                    continue
                elif k == "fcalias" and v != "":
                    fcaliasinfo = self.__get_fcalias_info_ssh(v)
                    if fcaliasinfo:
                        a = {}
                        a["ROW_fcalias_member"] = fcaliasinfo
                        mem_dict["TABLE_fcalias_member"] = a
                    mem_dict["fcalias_name"] = v  # get from fcaliaskeys
                    mem_dict["fcalias_vsan_id"] = int(
                        self._vsan
                    )  # get from fcaliaskeys
                else:
                    mem_dict[k] = v
            if mem_dict:
                retout.append(mem_dict)
        log.debug("After __format_members_ssh")
        log.debug(retout)
        return retout

    def __get_fcalias_info_ssh(self, fcaliasname):
        cmd = "show fcalias name " + fcaliasname + " vsan " + str(self._vsan)
        out = self.__swobj.show(cmd)
        retout = []
        for eachmem in out:
            mem_dict = {}
            if eachmem["fcalias_name"] == fcaliasname:
                for k, v in eachmem.items():
                    if (
                            k == "fcalias_member_type" and v == ""
                    ):  # if type is empty then exit from loop
                        break
                    elif (
                            k == "fcalias_name" or k == "fcalias_vsan_id" or v == ""
                    ):  # Dont req name/vsan or any value with null
                        continue
                    else:
                        mem_dict[k] = v
                if mem_dict:
                    retout.append(mem_dict)
        return retout

    def __format_members_ssh_active(self, out):
        # SSH o/p via textfsm template
        log.debug("Before __format_members_ssh_active")
        log.debug(out)
        retout = []
        for eachmem in out:
            mem_dict = {}
            for k, v in eachmem.items():
                if k == "vsan" or k == "zone_name" or v == "":
                    continue
                else:
                    mem_dict[k] = v
            if mem_dict:
                retout.append(mem_dict)
        log.debug("After __format_members_ssh_active")
        log.debug(retout)
        return retout

    @property
    def locked(self):
        """
        Check if zone lock is acquired

        :return: locked: True if zone lock is acquired else return False
        :rtype: bool
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.locked)
            False
            >>>
        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            self._lock_details = out[0]["session"]
        else:
            self._lock_details = out[get_key(zonekeys.SESSION, self._SW_VER)]
        if "none" in self._lock_details:
            return False
        else:
            return True

    @property
    def mode(self):
        """
        set zone mode or
        get zone mode

        :getter:
        :return: mode: get the current zone mode
        :rtype: str
        :example:
            >>>
            >>> print(zoneObj.mode)
            enhanced
            >>>

        :setter:
        :param mode: set zone mode
        :type mode: str
        :values: ['basic', 'enhanced']
        :raises CLIError: if vsan is not present on the switch
        :raises InvalidZoneMode: if zone mode is not ['basic', 'enhanced']
        :example:
            >>>
            >>> zoneObj.mode = 'enhanced'
            >>>

        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            return out[0]["mode"]
        return out[get_key(zonekeys.MODE, self._SW_VER)]

    @mode.setter
    def mode(self, value):
        cmd = (
                "terminal dont-ask ; zone mode "
                + ENHANCED
                + " vsan "
                + str(self._vsan)
                + " ; no terminal dont-ask"
        )
        if value.lower() == ENHANCED:
            self._send_zone_cmd(cmd)
        elif value.lower() == BASIC:
            cmd = cmd.replace("zone mode", "no zone mode")
            self._send_zone_cmd(cmd)
        else:
            raise InvalidZoneMode(
                "Invalid zone mode "
                + value
                + " . Valid values are: "
                + BASIC
                + ","
                + ENHANCED
            )

    @property
    def default_zone(self):
        """
        set default zone or
        get default zone

        :getter:
        :return: default_zone: default zone status
        :rtype: str
        :example:
            >>>
            >>> print(zoneObj.default_zone)
            deny
            >>>

        :setter:
        :param default_zone: set default zone value
        :type default_zone: str
        :values: ['permit', 'deny']
        :raises CLIError: if vsan is not present on the switch
        :raises InvalidDefaultZone: if def zone value is not ['permit', 'deny']
        :example:
            >>>
            >>> zoneObj.default_zone = "deny"
            >>>

        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            return out[0]["default_zone"]
        return out[get_key(zonekeys.DEFAULT_ZONE, self._SW_VER)]

    @default_zone.setter
    def default_zone(self, value):
        cmd = (
                "terminal dont-ask ; zone default-zone "
                + PERMIT
                + " vsan "
                + str(self._vsan)
                + " ; no terminal dont-ask"
        )
        if value.lower() == PERMIT:
            self._send_zone_cmd(cmd)
        elif value.lower() == DENY:
            cmd = cmd.replace("zone default-zone", "no zone default-zone")
            self._send_zone_cmd(cmd)
        else:
            raise InvalidDefaultZone(
                "Invalid default-zone value "
                + value
                + " . Valid values are: "
                + PERMIT
                + ","
                + DENY
            )

    @property
    def smart_zone(self):
        """
        set smart zone or
        get smart zone

        :getter:
        :return: smart_zone : True if smart zone is enabled, False otherwise
        :rtype: bool
        :example:
            >>>
            >>> print(zoneObj.smart_zone)
            True
            >>>

        :setter:
        :param smart_zone: enables smart zone if set to True, else disables it
        :type smart_zone: bool
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.smart_zone = True
            >>>

        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            val = out[0]["smart_zoning"]
        else:
            val = out[get_key(zonekeys.SMART_ZONE, self._SW_VER)]
        if val.lower() == "enabled":
            return True
        return False

    @smart_zone.setter
    def smart_zone(self, value):
        cmd = "zone smart-zoning enable vsan " + str(self._vsan)
        if type(value) is not bool:
            raise ValueError("Smart zone value must be of typr bool, True/False")
        if value:
            # If True then enable smart zoning
            cmd = "terminal dont-ask ; " + cmd + " ; no terminal dont-ask"
        else:
            # If False then disable smart zoning
            cmd = "terminal dont-ask ; no " + cmd + " ; no terminal dont-ask"
        self._send_zone_cmd(cmd)

    @property
    def fulldb_size(self):
        """
        Get full db size of the zone

        :return: fulldb_size: full db size of the zone
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_size)
            191
            >>>
        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["fulldb_dbsize"]
        else:
            retout = out.get(get_key(zonekeys.FULLDB_SIZE, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def fulldb_zone_count(self):
        """
        Get full db zone count

        :return: fulldb_zone_count:  full db zone count
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_zone_count)
            1
            >>>
        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["fulldb_zone_count"]
        else:
            retout = out.get(get_key(zonekeys.FULLDB_ZC, self._SW_VER), None)
        if type(retout) is int:
            return retout
        if retout:
            return int(retout)
        else:
            return None

    @property
    def fulldb_zoneset_count(self):
        """
        Get full db zoneset count

        :return: fulldb_zoneset_count: full db zoneset count
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_zoneset_count)
            0
            >>>
        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["fulldb_zoneset_count"]
        else:
            retout = out.get(get_key(zonekeys.FULLDB_ZSC, self._SW_VER), None)
        if type(retout) is int:
            return retout
        if retout:
            return int(retout)
        else:
            return None

    @property
    def activedb_size(self):
        """
        Get active db size of the zone

        :return: activedb_size: active db size of the zone, None if no active db
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_size)
            None
            >>>
        """
        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["activedb_dbsize"]
        else:
            retout = out.get(get_key(zonekeys.ACTIVEDB_SIZE, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def activedb_zone_count(self):
        """
        Get active db zone count

        :return: activedb_zone_count: active db zone count, None if no active db
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zone_count)
            None
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["activedb_zone_count"]
        else:
            retout = out.get(get_key(zonekeys.ACTIVEDB_ZC, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def activedb_zoneset_count(self):
        """
        Get active db zoneset count

        :return: activedb_zoneset_count: Returns active db zoneset count, None if no active db
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zoneset_count)
            None
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["activedb_zoneset_count"]
        else:
            retout = out.get(get_key(zonekeys.ACTIVEDB_ZSC, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def activedb_zoneset_name(self):
        """
        Get name of the active zoneset

        :return: activedb_zoneset_name: name of the active zoneset, else None
        :rtype: str
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zoneset_name)
            None
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["activedb_zoneset_name"]
            if not retout:
                return None
            return retout
        else:
            return out.get(get_key(zonekeys.ACTIVEDB_ZSN, self._SW_VER), None)

    @property
    def maxdb_size(self):
        """
        Get max db size of the zone

        :return: maxdb_size: max db size of the zone
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.maxdb_size)
            4000000
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["maxdb_dbsize"]
        else:
            retout = out.get(get_key(zonekeys.MAXDB_SIZE, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def effectivedb_size(self):
        """
        Get effective db size of the zone

        :return: effectivedb_size: effective db size of the zone
        :rtype: int
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.effectivedb_size)
            191
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["effectivedb_dbsize"]
        else:
            retout = out.get(get_key(zonekeys.EFFDB_SIZE, self._SW_VER), None)
        if retout:
            return int(retout)
        else:
            return None

    @property
    def effectivedb_size_percentage(self):
        """
        Get effective db size of the zone in percentage terms

        :return: effectivedb_size_percentage: Get effective db size of the zone in percentage terms
        :rtype: str
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.effectivedb_size_percentage)
            0%
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]["percent_effectivedbsize"]
        else:
            retout = out.get(get_key(zonekeys.EFFDB_PER, self._SW_VER), None)
        if retout is None:
            return None
        return str(retout) + "%"

    @property
    def status(self):
        """
        Get the latest status of the zone

        :return: status: the latest status of the zone
        :rtype: str
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.status)
            "Set Smart Zoning Policy complete at 16:03:19 IST Mar 19 2020
            >>>
        """

        out = self.__show_zone_status()
        if self.__swobj.is_connection_type_ssh():
            retout1 = out[0]["status"]
            retout2 = out[0]["status_at"]
            return retout1 + " " + retout2
        else:
            return out.get(get_key(zonekeys.STATUS, self._SW_VER), None)

    def clear_lock(self):
        """
        Clear zone lock if acquired

        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.clear_lock()
        """

        cmd = (
                "terminal dont-ask ; clear zone lock vsan  "
                + str(self._vsan)
                + " ; no terminal dont-ask"
        )
        out = self.__swobj.config(cmd)
        if out:
            if self.__swobj.is_connection_type_ssh():
                msg = out
            else:
                msg = out["msg"]
            if msg:
                if "Zone database not locked" in msg:
                    log.debug(msg)
                elif "No pending info found" in msg:
                    log.debug(msg)
                elif "Command will clear lock from the entire fabric" in msg:
                    log.debug(msg)
                else:
                    log.debug(msg)
                    raise CLIError(cmd, msg)

    def create(self):
        """
        Create zone

        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> zoneObj.create()
            >>>
        """

        cmd = "zone name " + self._name + " vsan " + str(self._vsan)
        self._send_zone_cmd(cmd)

    def delete(self):
        """
        Delete zone

        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> zoneObj.delete()
            >>>
        """

        cmd = "no zone name " + self._name + " vsan " + str(self._vsan)
        self._send_zone_cmd(cmd)

    def add_members(self, members):
        """
        Add members to the zone

        :param members: add members to the zone, there are 2 ways you can add members to the zone
            (1) a list of members - Fc/Port-channel interface object, device-alias, pwwn
            or
            (2) a dict of members - here key will be valid zone member type like "pwwn","device-alias","interface" etc..
        :type members: list or dict
        :raises CLIError: if vsan is not present on the switch
        :raises InvalidZoneMemberType: if zone member type is invalid
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> zoneObj.create()
            >>> int12 = Fc(sw, "fc1/2")
            >>> int13 = Fc(sw, "fc1/3")
            # add members as a list
            >>> zoneObj.add_members([int12, int13, "somename", "11:22:33:44:55:66:77:88"])
            >>>
            # add members as a dict
            >>> memlist = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
            ... {'pwwn': '50:08:01:60:08:9f:4d:01'},
            ... {'interface': int13.name},
            ... {'device-alias': 'hello'}, {'ip-address': '1.1.1.1'},
            ... {'symbolic-nodename': 'symbnodename'},
            ... {'fwwn': '11:12:13:14:15:16:17:18'}, {'fcid': '0x123456'},
            ... {'interface': int12.name},
            ... {'symbolic-nodename': 'testsymnode'},
            ... {'fcalias': 'somefcalias'}]
            >>> zoneObj.add_members(memlist)
            >>>
        """
        self.__add_remove_members(members)

    def remove_members(self, members):
        """
        Remove members from the zone

        :param members: Remove members from the zone, there are 2 ways you can remove members from the zone
            (1) a list of members - Fc/Port-channel interface object, device-alias, pwwn
            or
            (2) a dict of members - here key will be valid zone member type like "pwwn","device-alias","interface" etc..
        :type members: list or dict
        :raises CLIError: if vsan is not present on the switch
        :raises InvalidZoneMemberType: if zone member type is invalid
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,"zone_fab_a",1)
            >>> zoneObj.create()
            >>> int12 = Fc(sw, "fc1/2")
            >>> int13 = Fc(sw, "fc1/3")
            # Remove members as a list
            >>> zoneObj.remove_members([int12, int13, "somename", "11:22:33:44:55:66:77:88"])
            >>>
            # Remove members as a dict
            >>> memlist = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
            ... {'pwwn': '50:08:01:60:08:9f:4d:01'},
            ... {'interface': int13.name},
            ... {'device-alias': 'hello'}, {'ip-address': '1.1.1.1'},
            ... {'symbolic-nodename': 'symbnodename'},
            ... {'fwwn': '11:12:13:14:15:16:17:18'}, {'fcid': '0x123456'},
            ... {'interface': int12.name},
            ... {'symbolic-nodename': 'testsymnode'},
            ... {'fcalias': 'somefcalias'}]
            >>> zoneObj.remove_members(memlist)
            >>>
        """
        self.__add_remove_members(members, remove=True)

    def __add_remove_members(self, members, remove=False):

        cmdlist = []
        if self.__show_zone_name():
            cmdlist.append("zone name " + self._name + " vsan " + str(self._vsan))
            for eachmem in members:
                if (type(eachmem) is Fc) or (type(eachmem) is PortChannel):
                    name = eachmem.name
                    cmd = "member interface " + name
                    if remove:
                        cmd = "no " + cmd
                    cmdlist.append(cmd)
                elif type(eachmem) is str:
                    m = re.match(PAT_WWN, eachmem)
                    if m:
                        # zone member type is pwwn
                        cmd = "member pwwn " + eachmem
                        if remove:
                            cmd = "no " + cmd
                        cmdlist.append(cmd)
                    else:
                        # zone member type is of device-alias
                        cmd = "member device-alias " + eachmem
                        if remove:
                            cmd = "no " + cmd
                        cmdlist.append(cmd)
                elif type(eachmem) is dict:
                    cmd = self.__get_cmd_list(eachmem, remove)
                    cmdlist.append(cmd)
                else:
                    raise InvalidZoneMemberType(
                        "Invalid zone member type, currently we support member of type pwwn or device-alias or interface only"
                    )
            cmds_to_send = " ; ".join(cmdlist)
            self._send_zone_cmd(cmds_to_send)

    def __get_cmd_list(self, mem, removeflag):
        key = list(mem.keys())[0]
        val = list(mem.values())[0]
        valid_zone_members = get_key(zonekeys.VALID_MEMBERS, self._SW_VER)
        if key in list(valid_zone_members.keys()):
            cmd = "member " + key + " " + val
            if removeflag:
                cmd = "no " + cmd
            return cmd
        else:
            raise InvalidZoneMemberType(
                "Invalid zone member type ("
                + key
                + ") supported types are "
                + ", ".join(list(valid_zone_members.keys()))
            )

    def __show_zone_name(self):
        cmd = "show zone name " + self._name + " vsan  " + str(self._vsan)
        out = self._send_zone_show_cmd(cmd)
        return out

    def __show_zone_name_active(self):
        cmd = "show zone name " + self._name + " active vsan  " + str(self._vsan)
        out = self._send_zone_show_cmd(cmd)
        return out

    def __show_zone_status(self):
        cmd = "show zone status vsan  " + str(self._vsan)
        out = self._send_zone_show_cmd(cmd)
        if out:
            if self.__swobj.is_connection_type_ssh():
                return out
            else:
                retout = out["TABLE_zone_status"]["ROW_zone_status"]
                if type(retout) is list:
                    r = retout[0]
                else:
                    r = retout
            return r
        return out

    def _send_zone_show_cmd(self, cmd):
        try:
            out = self.__swobj.show(cmd)
        except CLIError as c:
            if "Zone not present" in c.message:
                # raise CLIError(cmd, out[0]) #Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
                return {}
            elif "Zoneset not present" in c.message:
                # raise CLIError(cmd, out[0]) #Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
                return {}
            else:
                raise CLIError(cmd, c.message)

        if out:
            if self.__swobj.is_connection_type_ssh():
                if type(out[0]) is str:
                    if (
                            "VSAN " + str(self._vsan) + " is not configured"
                            == out[0].strip()
                    ):
                        raise CLIError(cmd, out[0])
                    if "Zone not present" == out[0].strip():
                        # raise CLIError(cmd, out[0]) #Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
                        return {}
                    if "Zoneset not present" == out[0].strip():
                        # raise CLIError(cmd, out[0]) #Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
                        return {}
        return out

    def _send_zone_cmd(self, cmd):
        out = None
        msg = ""
        if self.locked:
            raise CLIError(
                cmd,
                "ERROR!! Zone lock is acquired. Lock details are: "
                + self._lock_details,
            )
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            if "Duplicate member" in c.message:
                return False, None
            self._check_msg(c.message, cmd)

        if out:
            if not self.__swobj.is_connection_type_ssh():
                msg = out["msg"].strip()
                if msg:
                    self._check_msg(msg, cmd)
        self.__commit_config_if_locked()

    def _check_msg(self, msg, cmd):
        if "Current zoning mode same as specified zoning mode" in msg:
            log.debug(msg)
        elif "Set zoning mode command initiated. Check zone status" in msg:
            log.debug(msg)
        elif "Enhanced zone session has been created" in msg:
            log.debug(msg)
        elif "No zone policy change" in msg:
            log.debug(msg)
        elif "Smart Zoning distribution initiated. check zone status" in msg:
            log.debug(msg)
        elif "Smart-zoning is already enabled" in msg:
            log.debug(msg)
        elif "Smart-zoning is already disabled" in msg:
            log.debug(msg)
        elif "Duplicate member" in msg:
            log.debug(msg)
        elif "Zoneset activation initiated" in msg:
            log.debug(msg)
        elif "Specified zoneset already active and unchanged" in msg:
            log.debug(msg)
        elif "Zoneset deactivation initiated" in msg:
            log.debug(msg)
        else:
            log.debug(msg)
            self._clear_lock_if_enhanced()
            raise CLIError(cmd, msg)

    def _clear_lock_if_enhanced(self):
        time.sleep(2)
        if self.mode == ENHANCED:
            self.clear_lock()

    def __commit_config_if_locked(self):
        time.sleep(1)
        if self.locked:
            log.debug("Sending commit cmd as lock is acquired")
            cmd = "show zone pending-diff vsan " + str(self._vsan)
            out = self.__swobj.show(cmd, raw_text=True)
            cmd = "zone commit vsan " + str(self._vsan)
            try:
                o = self.__swobj.config(cmd)
                if o is not None:
                    msg = o["msg"]
                    if msg:
                        if "Commit operation initiated. Check zone status" in msg:
                            return
                        elif "No pending info found" in msg:
                            return
                        else:
                            log.debug(msg)
                            raise CLIError(cmd, msg)
            except CLIError as c:
                msg = c.message
                if "Commit operation initiated. Check zone status" in msg:
                    return
                elif "No pending info found" in msg:
                    return
                else:
                    raise CLIError(cmd, msg)
