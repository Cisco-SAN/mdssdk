import logging
import re

import time

from .connection_manager.errors import CLIError, CustomException, VsanNotPresent
from .constants import ENHANCED, BASIC, PERMIT, DENY, PAT_WWN
from .fc import Fc
from .nxapikeys import zonekeys
from .portchannel import PortChannel
from .utility.utils import get_key

log = logging.getLogger(__name__)


# zone related exceptions
class InvalidZoneMode(CustomException):
    pass


class InvalidZoneMemberType(CustomException):
    pass


class Zone(object):
    """
    Zone module

    :param switch: switch object on which zone operations needs to be executed
    :type switch: Switch
    :param vsan: vsan object on which zone operations needs to be executed
    :type vsan: Vsan
    :param name: zone name with which zone operations needs to be executed
    :type name: str
    :raises VsanNotPresent: if vsan is not present on the switch
    :example:
        >>>
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
        >>> vsan_obj = Vsan(switch = switch_obj, id = 2)
        >>> vsan_obj.create()
        >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
        >>>
    """

    def __init__(self, switch, vsan, name):
        self.__swobj = switch
        self._SW_VER = switch._SW_VER
        self._vsanobj = vsan
        self._vsan = self._vsanobj.id
        if self._vsan is None:
            raise VsanNotPresent(
                "Vsan " + str(self._vsanobj._id) + " is not present on the switch. Please create the vsan first.")
        self._name = name
        self.__zones = None
        self.__rpc = None
        self.__method = u'cli_conf'

    @property
    def name(self):
        """
        Get zone name

        :return: name: Zone name
        :rtype: str
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
            >>> zoneObj.create()
            >>> print(zoneObj.name)
            zone_fab_a
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_name()
        if out:
            return out[get_key(zonekeys.NAME, self._SW_VER)]
        return None

    @property
    def vsan(self):
        """
        Get vsan object for the zone

        :return: vsan: vsan of the zone
        :rtype: Vsan
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> vsan_obj = Vsan(switch = switch_obj, id = 2)
            >>> vsan_obj.create()
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
            >>> vobj = zoneObj.vsan
            >>> print(vobj)
            <mdslib.vsan.Vsan object at 0x10d105550>
            >>> print(vobj.id)
            2
            >>>

        """
        if self.name is not None:
            return self._vsanobj
        return None

    @property
    def members(self):
        """
        Get members of the zone

        :return: members: members of the zone
        :rtype: list
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.members)
            [{'interface': 'fc1/2'}, {'interface': 'fc1/3'}, {'device-alias': 'somename'}, {'pwwn': '11:22:33:44:55:66:77:88'}]
            >>>

        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_name()
        if out:
            try:
                retout = out['TABLE_zone_member']['ROW_zone_member']
            except KeyError:
                return None
            if type(retout) is dict:
                # means there is only one member for the zone, so convert to list and return
                return self.__format_members([retout])
            return self.__format_members(retout)
        return None

    def __format_members(self, retout):

        #
        # This function converts the input retout from this
        #
        # [{'type': 'pwwn', 'wwn': '50:08:01:60:08:9f:4d:00', 'dev_alias': 'JDSU-180-Lrow-1'},
        #  {'type': 'pwwn', 'wwn': '50:08:01:60:08:9f:4d:01', 'dev_alias': 'JDSU-180-Lrow-2'},
        #  {'type': 'interface', 'intf_fc': 'fc1/4', 'wwn': '20:00:00:de:fb:b1:96:10'},
        #  {'type': 'device-alias', 'dev_alias': 'hello'}, {'type': 'ip-address', 'ipaddr': '1.1.1.1'},
        #  {'type': 'symbolic-nodename', 'symnodename': 'symbnodename'},
        #  {'type': 'fwwn', 'wwn': '11:12:13:14:15:16:17:18'}, {'type': 'fcid', 'fcid': '0x123456'},
        #  {'type': 'interface', 'intf_port_ch': 1, 'wwn': '20:00:00:de:fb:b1:96:10'},
        #  {'type': 'symbolic-nodename', 'symnodename': 'testsymnode'},
        #  {'type': 'fcalias', 'fcalias_name': 'somefcalias', 'fcalias_vsan_id': 1}]
        #
        # to this one
        #
        # [{'pwwn': '50:08:01:60:08:9f:4d:00'},
        #  {'pwwn': '50:08:01:60:08:9f:4d:01'},
        #  {'interface': 'fc1/4'},
        #  {'device-alias': 'hello'}, {'ip-address': '1.1.1.1'},
        #  {'symbolic-nodename': 'symbnodename'},
        #  {'fwwn': '11:12:13:14:15:16:17:18'}, {'fcid': '0x123456'},
        #  {'interface': 1},
        #  {'symbolic-nodename': 'testsymnode'},
        #  {'fcalias': 'somefcalias'}]
        log.debug(retout)
        retvalues = []
        valid_zone_members = get_key(zonekeys.VALID_MEMBERS, self._SW_VER)
        for eachmem in retout:
            type = eachmem[get_key(zonekeys.ZONE_MEMBER_TYPE, self._SW_VER)]
            nxapikey = valid_zone_members.get(type)
            for eachkey in eachmem.keys():
                if eachkey.startswith(nxapikey):
                    value = eachmem[eachkey]
                    retvalues.append({type: value})
        return retvalues

    @property
    def locked(self):
        """
        Check if zone lock is acquired

        :return: locked: True if zone lock is acquired else return False
        :rtype: bool
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.locked)
            False
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
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
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.mode = 'enhanced'
            >>>

        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[get_key(zonekeys.MODE, self._SW_VER)]

    @mode.setter
    def mode(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "terminal dont-ask ; zone mode " + ENHANCED + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == ENHANCED:
            self._send_zone_cmd(cmd)
        elif value.lower() == BASIC:
            cmd = cmd.replace("zone mode", "no zone mode")
            self._send_zone_cmd(cmd)
        else:
            raise InvalidZoneMode(
                "Invalid zone mode " + value + " . Valid values are: " + BASIC + "," + ENHANCED)

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
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.default_zone = "deny"
            >>>

        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[get_key(zonekeys.DEFAULT_ZONE, self._SW_VER)]

    @default_zone.setter
    def default_zone(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "terminal dont-ask ; zone default-zone " + PERMIT + " vsan " + str(
            self._vsan) + " ; no terminal dont-ask"
        if value.lower() == PERMIT:
            self._send_zone_cmd(cmd)
        elif value.lower() == DENY:
            cmd = cmd.replace("zone default-zone", "no zone default-zone")
            self._send_zone_cmd(cmd)
        else:
            raise CLIError("No cmd sent",
                           "Invalid default-zone value " + value + " . Valid values are: " + PERMIT + "," + DENY)

    @property
    def smart_zone(self):
        """
        set smart zone or
        get smart zone

        :getter:
        :return: smart_zone : get smart zone status
        :rtype: str
        :example:
            >>>
            >>> print(zoneObj.smart_zone)
            disabled
            >>>

        :setter:
        :param smart_zone: enables smart zone if set to True, else disables it
        :type smart_zone: bool
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.smart_zone = True
            >>>

        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out[get_key(zonekeys.SMART_ZONE, self._SW_VER)]

    @smart_zone.setter
    def smart_zone(self, value):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zone smart-zoning enable vsan " + str(self._vsan)
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
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_size)
            191
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.FULLDB_SIZE, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def fulldb_zone_count(self):
        """
        Get full db zone count

        :return: fulldb_zone_count:  full db zone count
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_zone_count)
            1
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.FULLDB_ZC, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def fulldb_zoneset_count(self):
        """
        Get full db zoneset count

        :return: fulldb_zoneset_count: full db zoneset count
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.fulldb_zoneset_count)
            0
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.FULLDB_ZSC, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def activedb_size(self):
        """
        Get active db size of the zone

        :return: activedb_size: active db size of the zone, None if no active db
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_size)
            None
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.ACTIVEDB_SIZE, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def activedb_zone_count(self):
        """
        Get active db zone count

        :return: activedb_zone_count: active db zone count, None if no active db
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zone_count)
            None
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.ACTIVEDB_ZC, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def activedb_zoneset_count(self):
        """
        Get active db zoneset count

        :return: activedb_zoneset_count: Returns active db zoneset count, None if no active db
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zoneset_count)
            None
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.ACTIVEDB_ZSC, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def activedb_zoneset_name(self):
        """
        Get name of the active zoneset

        :return: activedb_zoneset_name: name of the active zoneset, else None
        :rtype: str
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.activedb_zoneset_name)
            None
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out.get(get_key(zonekeys.ACTIVEDB_ZSN, self._SW_VER), None)

    @property
    def maxdb_size(self):
        """
        Get max db size of the zone

        :return: maxdb_size: max db size of the zone
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.maxdb_size)
            4000000
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.MAXDB_SIZE, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def effectivedb_size(self):
        """
        Get effective db size of the zone

        :return: effectivedb_size: effective db size of the zone
        :rtype: int
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.effectivedb_size)
            191
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.EFFDB_SIZE, self._SW_VER), None)
        if retout is not None:
            return int(retout)
        return None

    @property
    def effectivedb_size_percentage(self):
        """
        Get effective db size of the zone in percentage terms

        :return: effectivedb_size_percentage: Get effective db size of the zone in percentage terms
        :rtype: str
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.effectivedb_size_percentage)
            0%
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        retout = out.get(get_key(zonekeys.EFFDB_PER, self._SW_VER), None)
        if retout is not None:
            return str(retout) + "%"
        return None

    @property
    def status(self):
        """
        Get the latest status of the zone

        :return: status: the latest status of the zone
        :rtype: str
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zoneObj.status)
            "Set Smart Zoning Policy complete at 16:03:19 IST Mar 19 2020
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zone_status()
        return out.get(get_key(zonekeys.STATUS, self._SW_VER), None)

    def clear_lock(self):
        """
        Clear zone lock if acquired

        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj.clear_lock()
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "terminal dont-ask ; clear zone lock vsan  " + str(self._vsan) + " ; no terminal dont-ask"
        out = self.__swobj.config(cmd)
        if out is not None:
            msg = out['msg']
            if msg:
                if "Zone database not locked" in msg:
                    log.debug(msg)
                elif "No pending info found" in msg:
                    log.debug(msg)
                elif "Command will clear lock from the entire fabric" in msg:
                    log.debug(msg)
                else:
                    log.error(msg)
                    raise CLIError(cmd, msg)

    def create(self):
        """
        Create zone

        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
            >>> zoneObj.create()
            >>>
         """

        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zone name " + self._name + " vsan " + str(self._vsan)
        self._send_zone_cmd(cmd)

    def delete(self):
        """
        Delete zone

        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
            >>> zoneObj.delete()
            >>>
         """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
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
        :raises VsanNotPresent: if vsan is not present on the switch
        :raises InvalidZoneMemberType: if zone member type is invalid
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
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
        :raises VsanNotPresent: if vsan is not present on the switch
        :raises InvalidZoneMemberType: if zone member type is invalid
        :example:
            >>>
            >>> zoneObj = Zone(switch_obj,vsan_obj,"zone_fab_a")
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
        # TODO docstring
        self.__add_remove_members(members, remove=True)

    def __add_remove_members(self, members, remove=False):
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmdlist = []
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
                    "Invalid zone member type, currently we support member of type pwwn or device-alias or interface only")
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
                "Invalid zone member type (" + key + ") supported types are " + ', '.join(
                    list(valid_zone_members.keys())))

    def __show_zone_name(self):

        log.debug("Executing the cmd show zone name <> vsan <> ")
        cmd = "show zone name " + self._name + " vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out

    def __show_zone_status(self):
        log.debug("Executing the cmd show zone status vsan <> ")
        cmd = "show zone status vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out['TABLE_zone_status']['ROW_zone_status']

    def _send_zone_cmd(self, cmd):
        if self.locked:
            raise CLIError(cmd, "ERROR!! Zone lock is acquired. Lock details are: " + self._lock_details)
        try:
            out = self.__swobj.config(cmd)
            log.debug(out)
        except CLIError as c:
            if "Duplicate member" in c.message:
                return False, None
            log.error(c)
            raise CLIError(cmd, c.message)

        if out is not None:
            msg = out['msg'].strip()
            log.debug("------" + msg)
            if msg:
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
                    log.error(msg)
                    self._clear_lock_if_enhanced()
                    raise CLIError(cmd, msg)
        self.__commit_config_if_locked()

    def _clear_lock_if_enhanced(self):
        time.sleep(2)
        if self.mode == ENHANCED:
            self.clear_lock()

    def __commit_config_if_locked(self):
        time.sleep(2)
        if self.locked:
            log.debug("Sending commit cmd as lock is acquired")
            cmd = "show zone pending-diff vsan " + str(self._vsan)
            out = self.__swobj.show(cmd, raw_text=True)
            log.debug(out)
            cmd = "zone commit vsan " + str(self._vsan)
            log.debug("Executing the cmd " + cmd)
            try:
                o = self.__swobj.config(cmd)
                if o is not None:
                    msg = o['msg']
                    if msg:
                        if "Commit operation initiated. Check zone status" in msg:
                            return
                        else:
                            log.error(msg)
                            raise CLIError(cmd, msg)
            except CLIError as c:
                msg = c.message
                if "No pending info found" in msg:
                    return
                else:
                    raise CLIError(cmd, msg)
