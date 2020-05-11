import logging

import time

from .connection_manager.errors import CLIError, CustomException
from .nxapikeys import zonekeys
from .utility.utils import get_key
from .zone import Zone, VsanNotPresent

log = logging.getLogger(__name__)


class ZoneNotPresent(CustomException):
    pass


class ZoneSet(object):
    """
    Zoneset module

    :param switch: switch object on which zoneset operations needs to be executed
    :type switch: Switch
    :param vsan: vsan object on which zoneset operations needs to be executed
    :type vsan: Vsan
    :param name: zoneset name with which zoneset operations needs to be executed
    :type name: str
    :raises VsanNotPresent: if vsan is not present on the switch
    :example:
        >>>
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password)
        >>> vsan_obj = Vsan(switch = switch_obj, id = 2)
        >>> vsan_obj.create()
        >>> zonesetObj = ZoneSet(switch_obj,vsan_obj,"zoneset_fab_A")
        >>>
    """

    def __init__(self, switch, vsan_obj, name):
        self.__swobj = switch
        self._SW_VER = switch._SW_VER
        self._vsanobj = vsan_obj
        self._vsan = self._vsanobj.id
        if self._vsan is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        self._name = name
        # Create a dummy zone obj to send zoneset cmds, DO NOT use 'create' method with it!!
        log.debug("Creating a dummy zone object for the zoneset with name " + self._name)
        self.__zoneObj = Zone(self.__swobj, self._vsanobj, name=None)

    @property
    def name(self):
        """
        Get zoneset name

        :return: name: Zoneset name
        :rtype: str
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,vsan_obj,"zoneset_fab_A")
            >>> zonesetObj.create()
            >>> print(zonesetObj.name)
            zoneset_fab_A
            >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zoneset_name()
        if out:
            out = out.get('TABLE_zoneset').get('ROW_zoneset')
            return out[get_key(zonekeys.NAME, self._SW_VER)]
        return None

    @property
    def vsan(self):
        """
        Get vsan object for the zoneset

        :return: vsan: vsan of the zoneset
        :rtype: Vsan
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> vsan_obj = Vsan(switch = switch_obj, id = 2)
            >>> vsan_obj.create()
            >>> zonesetObj = ZoneSet(switch_obj,vsan_obj,"zoneset_fab_A")
            >>> vobj = zonesetObj.vsan
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
        Get members of the zoneset

        :return: members: members of the zoneset
        :rtype: dict(zone_name: Zone)
        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> print(zonesetObj.members)
            {'zonetemp': <mdslib.zone.Zone object at 0x10dfc3e50>, 'zonetemp_int': <mdslib.zone.Zone object at 0x10dfc3ed0>}
            >>>

        """
        retlist = {}
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        out = self.__show_zoneset_name()
        if out:
            zonesetdata = out.get('TABLE_zoneset', None).get('ROW_zoneset', None)
            if zonesetdata is not None:
                zonedata = zonesetdata.get('TABLE_zone', None)
                if zonedata is not None:
                    zdb = zonedata.get('ROW_zone', None)
                    if type(zdb) is dict:
                        zname = zdb[get_key(zonekeys.NAME, self._SW_VER)]
                        retlist[zname] = Zone(self.__swobj, self._vsanobj, zname)
                    else:
                        for eachzdb in zdb:
                            zname = eachzdb[get_key(zonekeys.NAME, self._SW_VER)]
                            retlist[zname] = Zone(self.__swobj, self._vsanobj, eachzdb)
                    return retlist
        return None

    def create(self):
        """
        Create zoneset

        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,vsan_obj,"zoneset_fab_A")
            >>> zonesetObj.create()
            >>>
         """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def delete(self):
        """
        Delete zoneset

        :raises VsanNotPresent: if vsan is not present on the switch
        :example:
            >>>
            >>> zonesetObj = ZoneSet(switch_obj,vsan_obj,"zoneset_fab_A")
            >>> zonesetObj.delete()
            >>>
         """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "no zoneset name " + self._name + " vsan " + str(self._vsan)
        self.__zoneObj._send_zone_cmd(cmd)

    def add_members(self, members):
        """
        Add members i.e zones to the zoneset

        :param members: list of Zone members that need to be added to zoneset
        :type members: list(Zone)
        :return: None
        :raises ZoneNotPresent: If zone is not present in the switch

        :example:
            >>>
            >>> z1 = Zone(sw, v, "zonetemp")
            >>> z2 = Zone(sw, v, "zonetemp_int")
            >>> z1.create()
            >>> z2.create()
            >>> zs = ZoneSet(switch=sw, vsan_obj=v, name="scriptZoneset")
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
        :raises ZoneNotPresent: If zone is not present in the switch

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
         :raises VsanNotPresent: if vsan is not present on the switch
         :example:
             >>>
             >>> # Activate the zoneset
             >>> zs.activate()
             >>> # Deactivate the zoneset
             >>> zs.activate(False)
             >>>
        """
        time.sleep(1)
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        if self.name is not None:
            if action:
                cmd = "terminal dont-ask ; zoneset activate name " + self._name + " vsan " + str(
                    self._vsan) + " ; no terminal dont-ask"
            else:
                cmd = "terminal dont-ask ; no zoneset activate name " + self._name + " vsan " + str(
                    self._vsan) + " ; no terminal dont-ask"
            try:
                self.__zoneObj._send_zone_cmd(cmd)
            except CLIError as c:
                if "Fabric unstable" in c.message:
                    log.error("Fabric is currently unstable, executing activation after few secs")
                    time.sleep(5)
                    self.__zoneObj._send_zone_cmd(cmd)

    def is_active(self):
        """
         Check if the zoneset is active or not

         :return: True if zoneset is active, False otherwise
         :rtype: bool
         :raises VsanNotPresent: if vsan is not present on the switch
         :example:
             >>>
             >>> zs.is_active()
             True
             >>>
        """
        if self._vsanobj.id is None:
            raise VsanNotPresent("Vsan " + str(self._vsanobj._id) + " is not present on the switch.")
        cmd = "show zoneset active vsan " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        if out:
            azsdetails = out['TABLE_zoneset']['ROW_zoneset']
            azs = azsdetails[get_key(zonekeys.NAME, self._SW_VER)]
            if azs == self._name:
                return True
        return False

    def __add_remove_members(self, members, remove=False):
        cmdlist = []
        cmdlist.append("zoneset name " + self._name + " vsan " + str(self._vsan))
        for eachmem in members:
            name_of_zone = eachmem.name
            if name_of_zone is None:
                self.__zoneObj._clear_lock_if_enhanced()
                raise ZoneNotPresent(
                    "The given zoneset member '" + eachmem._name + "' is not present in the switch. Please create the zone first.")
            else:
                if remove:
                    cmd = "no member " + name_of_zone
                else:
                    cmd = "member " + name_of_zone
                cmdlist.append(cmd)
        cmds_to_send = " ; ".join(cmdlist)
        out = self.__zoneObj._send_zone_cmd(cmds_to_send)

    def __show_zoneset_name(self):
        log.debug("Executing the cmd show zone name <> vsan <> ")
        cmd = "show zoneset name " + self._name + " vsan  " + str(self._vsan)
        out = self.__swobj.show(cmd)
        log.debug(out)
        # print(out)
        return out
