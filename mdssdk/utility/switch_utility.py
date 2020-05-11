import logging
import re

from .utils import get_key
from .. import constants
from ..fc import Fc
from ..module import Module
from ..nxapikeys import interfacekeys, vsankeys, zonekeys, modulekeys
from ..portchannel import PortChannel
from ..vsan import Vsan
from ..zone import Zone

log = logging.getLogger(__name__)


class SwitchUtils:

    @property
    def interfaces(self):
        """
        Returns all the interfaces of the switch in dictionary format(interface name:interface object)

        :return: Returns all the interfaces(Fc and PortChannel) on the switch in dictionary format(interface name:interface object)
        :rtype: dict(name:Interface(Fc or PortChannel)
        :example:
            >>> allint = switch_obj.interfaces
            >>> print(allint)
            {'fc1/1': <mdslib.fc.Fc object at 0x10bd5da90>, 'fc1/2': <mdslib.fc.Fc object at 0x10bde4050>, 'fc1/3': <mdslib.fc.Fc object at 0x10bd5d650>,
             'fc1/4': <mdslib.fc.Fc object at 0x10bd5df90>, 'fc1/5': <mdslib.fc.Fc object at 0x10bd5d9d0>, .....
             'port-channel212': <mdslib.portchannel.PortChannel object at 0x10d88ee90>, 'port-channel213': <mdslib.portchannel.PortChannel object at 0x10d88eed0>,
             'port-channel214': <mdslib.portchannel.PortChannel object at 0x10d88ef50>}
            >>>
        """
        retlist = {}
        cmd = "show interface brief"
        out = self.show(cmd)
        log.debug(out)

        # Get FC related data
        fcout = out.get('TABLE_interface_brief_fc', None)
        if fcout is not None:
            allfc = fcout['ROW_interface_brief_fc']
            if type(allfc) is dict:
                allfc = [allfc]
            for eacfc in allfc:
                fcname = eacfc[get_key(interfacekeys.INTERFACE, self._SW_VER)]
                fcobj = Fc(switch=self, name=fcname)
                retlist[fcname] = fcobj

        # Get PC related data
        pcout = out.get('TABLE_interface_brief_portchannel', None)
        if pcout is not None:
            allpc = pcout['ROW_interface_brief_portchannel']
            if type(allpc) is dict:
                allpc = [allpc]
            for eacpc in allpc:
                pcname = eacpc[get_key(interfacekeys.INTERFACE, self._SW_VER)]
                match = re.match(constants.PAT_PC, pcname)
                if match:
                    pcid = int(match.group(1))
                    pcobj = PortChannel(switch=self, id=pcid)
                    retlist[pcname] = pcobj
        return retlist

    @property
    def vsans(self):
        """
        Returns all the vsans present on the switch in dictionary format(vsan-id:vsan object)

        :return: Returns all the vsans present on the switch in dictionary format(vsan-id:vsan object)
        :rtype: dict(vsan-id : Vsan)
        :example:
            >>> allvsans = switch_obj.vsans
            >>> print(allvsans)
            {'1': <mdslib.vsan.Vsan object at 0x10d88a290>, '10': <mdslib.vsan.Vsan object at 0x10d88a1d0>,
             '11': <mdslib.vsan.Vsan object at 0x10d88a150>,  .....
             '499': <mdslib.vsan.Vsan object at 0x10bdee650>, '4079': <mdslib.vsan.Vsan object at 0x10bdee0d0>,
             '4094': <mdslib.vsan.Vsan object at 0x10bdee150>}
            >>>
        """
        retlist = {}
        cmd = "show vsan"
        out = self.show(cmd)['TABLE_vsan']['ROW_vsan']
        for eachele in out:
            id = eachele.get(get_key(vsankeys.VSAN_ID, self._SW_VER))
            vobj = Vsan(switch=self, id=id)
            retlist[id] = vobj
        return retlist

    @property
    def zonesets(self):
        if self.npv:
            return None
        # TODO
        raise NotImplementedError

    @property
    def zones(self):
        if self.npv:
            return None
        # TODO
        retlist = {}
        cmd = "show zone"
        out = self.show(cmd)
        if out:
            allzones = out['TABLE_zone']['ROW_zone']
            if type(allzones) is dict:
                allzones = [allzones]
            log.warning("There are a total of " + str(
                len(allzones)) + " zones across vsans. Please wait while we get the zone info...")
            for eachzone in allzones:
                vsanid = eachzone.get(get_key(zonekeys.VSAN_ID, self._SW_VER))
                vobj = Vsan(switch=self, id=vsanid)
                zname = eachzone.get(get_key(zonekeys.NAME, self._SW_VER))
                zobj = Zone(switch=self, vsan_obj=vobj, name=zname)
                listofzones = retlist.get(vsanid, None)
                # print(vsanid)
                # print(zname)
                if listofzones is None:
                    listofzones = [zobj]
                else:
                    listofzones.append(zobj)
                retlist[vsanid] = listofzones
            return retlist
        return None

    @property
    def modules(self):
        """
        Returns a list of modules present on the switch

        :return: list of modules present on the switch
        :rtype: list(Module)
        :example:
            >>> mods = switch_obj.modules
            >>> for eachmod in mods:
            ...     print("mod status is    : " + eachmod.status)
            ...     print("mod ports is     : " + str(eachmod.ports))
            ...     print("mod modtype is   : " + eachmod.module_type)
            ...     print("mod model is     : " + eachmod.model)
            ...     print("mod modnumber is : " + str(eachmod.module_number))
            ...     print("##")
            >>>
            >>>
            mod status is    : ok
            mod ports is     : 48
            mod modtype is   : 2/4/8/10/16 Gbps Advanced FC Module
            mod model is     : DS-X9448-768K9
            mod modnumber is : 1
            ##
            mod status is    : ok
            mod ports is     : 48
            mod modtype is   : 4/8/16/32 Gbps Advanced FC Module
            mod model is     : DS-X9648-1536K9
            mod modnumber is : 3
            ##
            mod status is    : ok
            mod ports is     : 48
            mod modtype is   : 2/4/8/10/16 Gbps Advanced FC Module
            mod model is     : DS-X9448-768K9
            mod modnumber is : 4
            ##
            mod status is    : active
            mod ports is     : 0
            mod modtype is   : Supervisor Module-3
            mod model is     : DS-X97-SF1-K9
            mod modnumber is : 5
            >>>
        """

        mlist = []
        out = self.show("show module")
        if not out:
            return None
        modinfo = out['TABLE_modinfo']['ROW_modinfo']
        # For 1RU switch modinfo is a dict
        if type(modinfo) is dict:
            modinfo = [modinfo]

        for eachmodinfo in modinfo:
            modnumkey = get_key(modulekeys.MOD_NUM, self._SW_VER)
            m = Module(self, eachmodinfo[modnumkey], eachmodinfo)
            mlist.append(m)
        return mlist

    @property
    def flogidb(self):
        if self.npv:
            cmd = "show npv flogi-table"
            out = self.show(cmd, raw_text=True)
            return out
        cmd = "show flogi database"
        out = self.show(cmd)
        return out

    @property
    def fcnsdb(self):
        if self.npv:
            return None
        cmd = "show fcns database"
        out = self.show(cmd)
        return out
