import logging

import time

from .connection_manager.errors import CLIError, UnsupportedSwitch
from .nxapikeys import zonekeys
from .parsers.zoneset import ShowZonesetActive
from .utility.utils import get_key
from .vsan import Vsan
from .zone import Zone
from .constants import VALID_PIDS_MDS

log = logging.getLogger(__name__)


class ZoneSet(object):
    """
    Zoneset module

    :param switch: switch object on which zoneset operations needs to be executed
    :type switch: Switch
    :param name: zoneset name with which zoneset operations needs to be executed
    :type name: str
    :param vsan: vsan id on which zone operations needs to be executed
    :type vsan: int
    :raises CLIError: if vsan is not present on the switch
    :example:
        >>>
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
        >>> zonesetObj = ZoneSet(switch_obj,"zoneset_fab_A",1)
        >>>
    """

    def __init__(self, switch, name, vsan):
        self.__swobj = switch
        self._SW_VER = switch._SW_VER
        self._vsan = vsan
        self._name = name
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )
        # Create a dummy zone obj to send zoneset cmds, DO NOT use 'create' method with it!!
        log.debug(
            "Init a dummy zone object for the zoneset with name "
            + self._name
            + " and vsan "
            + str(self._vsan)
        )
        self.__zoneObj = Zone(self.__swobj, name=None, vsan=self._vsan)

    @property
    def name(self):
        """
        Get zoneset name

        :return: name: Zoneset name
        :rtype: str
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,"zoneset_fab_A",1)
            >>> zonesetObj.create()
            >>> print(zonesetObj.name)
            zoneset_fab_A
            >>>
        """
        out = self.__show_zoneset_name_brief()
        if out:
            if self.__swobj.is_connection_type_ssh():
                return out[0]["zonesetname"]
            else:
                out = out.get("TABLE_zoneset").get("ROW_zoneset")
                if type(out) is list:
                    out = out[0]
                return out[get_key(zonekeys.NAME, self._SW_VER)]
        return None

    @property
    def vsan(self):
        """
        Get vsan object for the zoneset

        :return: vsan: vsan of the zoneset
        :rtype: Vsan
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,"zoneset_fab_A",1)
            >>> vobj = zonesetObj.vsan
            >>> print(vobj)
            <mdslib.vsan.Vsan object at 0x10d105550>
            >>>

        """
        vsan_obj = Vsan(switch=self.__swobj, id=self._vsan)
        return vsan_obj

    @property
    def members(self):
        """
        Get members of the zoneset

        :return: members: members of the zoneset
        :rtype: dict(zone_name: Zone)
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zonesetObj.members)
            {'zonetemp': <mdslib.zone.Zone object at 0x10dfc3e50>, 'zonetemp_int': <mdslib.zone.Zone object at 0x10dfc3ed0>}
            >>>

        """
        retlist = {}
        out = self.__show_zoneset_name_brief()
        if out:
            if self.__swobj.is_connection_type_ssh():
                members = out[0]["zonename"]
                for eachzmem in members:
                    zobj = Zone(self.__swobj, eachzmem, self._vsan)
                    retlist[eachzmem] = zobj
            else:
                zonesetdata = out.get("TABLE_zoneset", None).get("ROW_zoneset", None)
                if zonesetdata is not None:
                    if type(zonesetdata) is list:
                        zonesetdata = zonesetdata[0]
                    zonedata = zonesetdata.get("TABLE_zone", None)
                    if zonedata is not None:
                        zdb = zonedata.get("ROW_zone", None)
                        if type(zdb) is dict:
                            zname = zdb[get_key(zonekeys.NAME, self._SW_VER)]
                            zobj = Zone(self.__swobj, zname, self._vsan)
                            retlist[zname] = zobj
                        else:
                            for eachzdb in zdb:
                                zname = eachzdb[get_key(zonekeys.NAME, self._SW_VER)]
                                zobj = Zone(self.__swobj, zname, self._vsan)
                                retlist[zname] = zobj
        return retlist

    @property
    def active_members(self):
        """
        Get members of the active zoneset if any

        :return: members: members active zoneset if any
        :rtype: dict(zone_name: Zone)
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zonesetObj.active_members)
            {'zonetemp': <mdslib.zone.Zone object at 0x10dfc3e50>, 'zonetemp_int': <mdslib.zone.Zone object at 0x10dfc3ed0>}
            >>>

        """
        retlist = {}
        out = self.__show_zoneset_name_brief(active=True)
        if out:
            if self.__swobj.is_connection_type_ssh():
                members = out[0]["zonename"]
                for eachzmem in members:
                    zobj = Zone(self.__swobj, eachzmem, self._vsan)
                    retlist[eachzmem] = zobj
            else:
                zonesetdata = out.get("TABLE_zoneset", None).get("ROW_zoneset", None)
                if zonesetdata is not None:
                    zonedata = zonesetdata.get("TABLE_zone", None)
                    if zonedata is not None:
                        zdb = zonedata.get("ROW_zone", None)
                        if type(zdb) is dict:
                            zname = zdb[get_key(zonekeys.NAME, self._SW_VER)]
                            zobj = Zone(self.__swobj, zname, self._vsan)
                            retlist[zname] = zobj
                        else:
                            for eachzdb in zdb:
                                zname = eachzdb[get_key(zonekeys.NAME, self._SW_VER)]
                                zobj = Zone(self.__swobj, zname, self._vsan)
                                retlist[zname] = zobj
        return retlist

    def create(self):
        """
        Create zoneset

        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,"zoneset_fab_A",1)
            >>> zonesetObj.create()
            >>>
        """
        cmd = "zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def delete(self):
        """
        Delete zoneset

        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,"zoneset_fab_A",1)
            >>> zonesetObj.delete()
            >>>
        """
        cmd = "no zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def add_members(self, members):
        """
        Add members i.e zones to the zoneset

        :param members: list of Zone members that need to be added to zoneset
        :type members: list(Zone)
        :return: None
        :raises CLIError: If zone is not present in the switch

        :example:
            >>>
            >>> z1 = Zone(sw,"zonetemp",1)
            >>> z2 = Zone(sw,"zonetemp_int",1)
            >>> z1.create()
            >>> z2.create()
            >>> zs = ZoneSet(switch=sw, name="scriptZoneset",vsan=1)
            >>> zs.create()
            >>> zs.add_members([z1,z2])
            >>>
        """
        self.__add_remove_members(members)

    def remove_members(self, members):
        """
        Remove members i.e zones from the zoneset

        :param members: list of Zone members that need to be removed from the zoneset
        :type members: list(Zone)
        :return: None
        :raises CLIError: If zone is not present in the switch

        :example:
            >>>
            >>> zs.remove_members([z1,z2])
            >>>
        """
        self.__add_remove_members(members, remove=True)

    def activate(self, action=True):
        """
        Activate or deactivate a zoneset

        :param action: activate zoneset if set to True, else deactivate the zoneset
        :type action: bool (deafult: True)
        :return: None
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> # Activate the zoneset
            >>> zs.activate()
            >>> # Deactivate the zoneset
            >>> zs.activate(False)
            >>>
        """
        time.sleep(1)
        if self.name is not None:
            if action:
                cmd = (
                        "terminal dont-ask ; zoneset activate name "
                        + self._name
                        + " vsan "
                        + str(self._vsan)
                        + " ; no terminal dont-ask"
                )
            else:
                cmd = (
                        "terminal dont-ask ; no zoneset activate name "
                        + self._name
                        + " vsan "
                        + str(self._vsan)
                        + " ; no terminal dont-ask"
                )
            try:
                self.__zoneObj._send_zone_cmd(cmd)
            except CLIError as c:
                if "Fabric unstable" in c.message:
                    log.error(
                        "Fabric is currently unstable, executing activation after few secs"
                    )
                    time.sleep(5)
                    self.__zoneObj._send_zone_cmd(cmd)

    def is_active(self):
        """
        Check if the zoneset is active or not

        :return: True if zoneset is active, False otherwise
        :rtype: bool
        :raises CLIError: if vsan is not present on the switch
        :example:
            >>>
            >>> zs.is_active()
            True
            >>>
        """
        cmd = "show zoneset active vsan " + str(self._vsan)
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show(cmd)
            shzoneset = ShowZonesetActive(outlines)
            if shzoneset.active == self._name:
                return True
            return False
        try:
            out = self.__swobj.show(cmd)
        except CLIError as c:
            if "Zoneset not present" in c.message:
                return False
        if out:
            azsdetails = out["TABLE_zoneset"]["ROW_zoneset"]
            if type(azsdetails) is list:
                azsdetails = azsdetails[0]
            azs = azsdetails[get_key(zonekeys.NAME, self._SW_VER)]
            if azs == self._name:
                return True
        return False

    def __add_remove_members(self, members, remove=False):
        if self.__show_zoneset_name_brief:
            cmdlist = []
            cmdlist.append("zoneset name " + self._name + " vsan " + str(self._vsan))
            for eachmem in members:
                name_of_zone = eachmem.name
                if name_of_zone:
                    if remove:
                        cmd = "no member " + name_of_zone
                    else:
                        cmd = "member " + name_of_zone
                    cmdlist.append(cmd)
            cmds_to_send = " ; ".join(cmdlist)
            out = self.__zoneObj._send_zone_cmd(cmds_to_send)

    def __show_zoneset_name_brief(self, active=False):
        if active:
            cmd = (
                    "show zoneset name "
                    + self._name
                    + " brief active vsan "
                    + str(self._vsan)
            )
        else:
            cmd = "show zoneset name " + self._name + " brief vsan " + str(self._vsan)

        out = self.__zoneObj._send_zone_show_cmd(cmd)
        return out

# TODO active members and members when zs is not present
# TODO in zone module to add active members
