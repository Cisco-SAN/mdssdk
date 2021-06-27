import logging
import re
import concurrent.futures

from .utils import get_key
from .. import constants
from ..fc import Fc
from ..module import Module
from ..nxapikeys import interfacekeys, vsankeys, zonekeys, modulekeys, inventorykeys
from ..parsers.interface import ShowInterfaceBrief
from ..parsers.vsan import ShowVsan
from ..portchannel import PortChannel
from ..zoneset import ZoneSet
from ..zone import Zone
from ..vsan import Vsan

log = logging.getLogger(__name__)


class SwitchUtils:

    def _is_mds_switch(self):
        self.__supported = False
        cmd = "show inventory"
        if self.connection_type != "ssh":
            inv = self.show(command=cmd,use_ssh=False)
            self.inv_details = inv['TABLE_inv']['ROW_inv']
        else:
            inv = self.show(command=cmd,use_ssh=True)
            self.inv_details = inv
        for eachline in self.inv_details:
            if eachline['name'] == 'Chassis':
                # Not using get_key here because this is run before we get the sw version
                # Hence 'productid' is hardcoded here
                self._product_id = eachline['productid']
                self._serial_num = eachline['serialnum']
                # 'DS-' is for MDS switches and 89 is for Raven switches
                if self.product_id.startswith("DS-") or self.product_id.startswith("89"):
                    self.__supported = True
                return self.__supported
        return self.__supported

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
        out = self.show(cmd, timeout=280)
        if self.is_connection_type_ssh():
            allfc, allpc = ShowInterfaceBrief(out).interfaces
            for fcname in allfc:
                fcobj = Fc(switch=self, name=fcname)
                retlist[fcname] = fcobj
            for pcname in allpc:
                match = re.match(constants.PAT_PC, pcname)
                if match:
                    pcid = int(match.group(1))
                    pcobj = PortChannel(switch=self, id=pcid)
                    retlist[pcname] = pcobj
            return retlist

        # Get FC related data
        fcout = out.get("TABLE_interface_brief_fc", None)
        if fcout is not None:
            allfc = fcout["ROW_interface_brief_fc"]
            if type(allfc) is dict:
                allfc = [allfc]
            for eacfc in allfc:
                fcname = eacfc[get_key(interfacekeys.INTERFACE, self._SW_VER)]
                fcobj = Fc(switch=self, name=fcname)
                retlist[fcname] = fcobj

        # Get PC related data
        pcout = out.get("TABLE_interface_brief_portchannel", None)
        if pcout is not None:
            allpc = pcout["ROW_interface_brief_portchannel"]
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
        if self.is_connection_type_ssh():
            outlines = self.show(cmd)
            shvsan = ShowVsan(outlines)
            out = shvsan.vsans
            for eachele in out:
                id = int(eachele.get("vsan"))
                vobj = Vsan(switch=self, id=id)
                retlist[int(id)] = vobj
            return retlist
        out = self.show(cmd)["TABLE_vsan"]["ROW_vsan"]
        for eachele in out:
            id = eachele.get(get_key(vsankeys.VSAN_ID, self._SW_VER))
            vobj = Vsan(switch=self, id=id)
            retlist[int(id)] = vobj
        return retlist

    @property
    def zonesets(self):
        if self.npv:
            return None
        return self._get_zs()

    @property
    def active_zonesets(self):
        """
        Returns all the active zonesets present on the switch in dictionary format(vsan-id:zoneset object)

        :return: Returns all the active zonesets present on the switch in dictionary format(vsan-id:zoneset object)
        :rtype: dict(vsan-id : ZoneSet)
        :example:
            >>> print(switch_obj.active_zonesets)
            {2: [<mdssdk.zoneset.ZoneSet object at 0x7f0c6f8b0c50>]}
            >>>
        """
        if self.npv:
            return None
        return self._get_zs(active=True)

    def _get_zs(self, active=False):
        retdict = {}
        if active:
            cmd = "show zoneset brief active"
        else:
            cmd = "show zoneset brief"
        out = self.show(cmd)
        if self.is_connection_type_ssh():
            for eachrow in out:
                v = int(eachrow['vsan'])
                zsname = eachrow['zonesetname']
                zsobj = ZoneSet(self, zsname, v)
                values = retdict.get(v, None)
                if values is None:
                    retdict[v] = [zsobj]
                else:
                    values.append(zsobj)
                    retdict[v] = values
        else:
            try:
                newout = out['TABLE_zoneset']['ROW_zoneset']
            except KeyError:
                return retdict
            if type(newout) is dict:
                newout = [newout]
            for eachrow in newout:
                v = int(eachrow.get(get_key(zonekeys.VSAN_ID, self._SW_VER)))
                zsname = eachrow.get(get_key(zonekeys.NAME, self._SW_VER))
                zsobj = ZoneSet(self, zsname, v)
                values = retdict.get(v, None)
                if values is None:
                    retdict[v] = [zsobj]
                else:
                    values.append(zsobj)
                    retdict[v] = values
        return retdict

    def _return_zone_obj_nxapi(self, eachzone):
        vsanid = eachzone.get(get_key(zonekeys.VSAN_ID, self._SW_VER))
        zname = eachzone.get(get_key(zonekeys.NAME, self._SW_VER))
        # zobj = zname
        zobj = Zone(switch=self, vsan=vsanid, name=zname, check_npv=False)
        return (vsanid, zobj)

    def _return_zone_obj_ssh(self, eachzone):
        # print(eachzone)
        zname, vsanid = eachzone
        zobj = Zone(switch=self, vsan=vsanid, name=zname, check_npv=False)
        return (vsanid, zobj)

    @property
    def zones(self):
        if self.npv:
            return {}
        cmd = "show zone"
        out = self.show(cmd)
        retlist = {}
        results = []
        if out:
            if self.is_connection_type_ssh():
                zone_vsan_dict = {}
                for eachzone in out:
                    vsan = eachzone.get("vsan")
                    zone_name = eachzone.get("zone_name")
                    zone_vsan_dict[zone_name] = int(vsan)
                allzones = list(zone_vsan_dict.items())
                print(
                    "There are a total of "
                    + str(len(zone_vsan_dict.items()))
                    + " zones across vsan(s). Please wait while we get the zone info..."
                )
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(self._return_zone_obj_ssh, allzones)
                    # zone_vsan_dict = {}
                    # for r in results:
                    #     vsan, zname = r
                    #     zone_vsan_dict[zname] = int(vsan)

                # for zone, vsanid in zone_vsan_dict.items():
                #     # vobj = Vsan(switch=self, id=vsanid)
                #     zobj = zone
                #     # zobj = Zone(switch=self, vsan=vobj, name=zname)
                #     listofzones = retlist.get(vsanid, None)
                #     if listofzones is None:
                #         listofzones = [zobj]
                #     else:
                #         listofzones.append(zobj)
                #     retlist[vsanid] = listofzones
            else:
                allzones = out["TABLE_zone"]["ROW_zone"]
                if type(allzones) is dict:
                    allzones = [allzones]
                print(
                    "There are a total of "
                    + str(len(allzones))
                    + " zones across vsan(s). Please wait while we get the zone info..."
                )
                # for eachzone in allzones:
                #     vsanid = eachzone.get(get_key(zonekeys.VSAN_ID, self._SW_VER))
                #     # vobj = Vsan(switch=self, id=vsanid)
                #     zname = eachzone.get(get_key(zonekeys.NAME, self._SW_VER))
                #     zobj = zname
                #     # zobj = Zone(switch=self, vsan=vobj, name=zname)
                #     listofzones = retlist.get(vsanid, None)
                #     if listofzones is None:
                #         listofzones = [zobj]
                #     else:
                #         listofzones.append(zobj)
                #     retlist[vsanid] = listofzones
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(self._return_zone_obj_nxapi, allzones)

        if results:
            for r in results:
                vsanid, zobj = r
                listofzones = retlist.get(vsanid, None)
                if listofzones is None:
                    listofzones = [zobj]
                else:
                    listofzones.append(zobj)
                retlist[vsanid] = listofzones
        return retlist

    # @property
    # def zones(self):
    #     if self.npv:
    #         return {}
    #     cmd = "show zone"
    #     out = self.show(cmd)
    #     retlist = {}
    #     if out:
    #         if self.is_connection_type_ssh():
    #             zone_vsan_dict = {}
    #             for eachzone in out:
    #                 vsan = eachzone.get("vsan")
    #                 zone_name = eachzone.get("zone_name")
    #                 zone_vsan_dict[zone_name] = int(vsan)
    #
    #             # with concurrent.futures.ThreadPoolExecutor() as executor:
    #             #     results = executor.map(self._return_zone_obj_ssh,out)
    #             #     zone_vsan_dict = {}
    #             #     for r in results:
    #             #         vsan, zname = r
    #             #         zone_vsan_dict[zname] = int(vsan)
    #             print(
    #                 "There are a total of "
    #                 + str(len(zone_vsan_dict.items()))
    #                 + " zones across vsan(s). Please wait while we get the zone info..."
    #             )
    #             for zone, vsanid in zone_vsan_dict.items():
    #                 # vobj = Vsan(switch=self, id=vsanid)
    #                 zobj = zone
    #                 # zobj = Zone(switch=self, vsan=vobj, name=zname)
    #                 listofzones = retlist.get(vsanid, None)
    #                 if listofzones is None:
    #                     listofzones = [zobj]
    #                 else:
    #                     listofzones.append(zobj)
    #                 retlist[vsanid] = listofzones
    #         else:
    #             allzones = out["TABLE_zone"]["ROW_zone"]
    #             if type(allzones) is dict:
    #                 allzones = [allzones]
    #             print(
    #                 "There are a total of "
    #                 + str(len(allzones))
    #                 + " zones across vsan(s). Please wait while we get the zone info..."
    #             )
    #             for eachzone in allzones:
    #                 vsanid = eachzone.get(get_key(zonekeys.VSAN_ID, self._SW_VER))
    #                 # vobj = Vsan(switch=self, id=vsanid)
    #                 zname = eachzone.get(get_key(zonekeys.NAME, self._SW_VER))
    #                 zobj = zname
    #                 # zobj = Zone(switch=self, vsan=vobj, name=zname)
    #                 listofzones = retlist.get(vsanid, None)
    #                 if listofzones is None:
    #                     listofzones = [zobj]
    #                 else:
    #                     listofzones.append(zobj)
    #                 retlist[vsanid] = listofzones
    #             # with concurrent.futures.ThreadPoolExecutor() as executor:
    #             #     results = executor.map(self._return_zone_obj_nxapi,allzones)
    #             #     for r in results:
    #             #         vsanid,zobj = r
    #             #         listofzones = retlist.get(vsanid, None)
    #             #         if listofzones is None:
    #             #             listofzones = [zobj]
    #             #         else:
    #             #             listofzones.append(zobj)
    #             #         retlist[vsanid] = listofzones
    #     return retlist

    @property
    def modules(self):
        """
        Returns a list of modules present on the switch

        :return: list of modules present on the switch
        :rtype: dict(module-num : Module)
        :example:
            >>> mods = switch_obj.modules
            >>> for modnum, eachmod in mods.items():
            ...     print("mod status is    : " + eachmod.status)
            ...     print("mod ports is     : " + str(eachmod.ports))
            ...     print("mod modtype is   : " + eachmod.type)
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

        mret = {}
        out = self.show("show module")
        if self.is_connection_type_ssh():
            for eachrow in out:
                modnum = eachrow["module"]
                m = Module(self, modnum, eachrow)
                mret[int(modnum)] = m
        else:
            modinfo = out["TABLE_modinfo"]["ROW_modinfo"]
            # For 1RU switch modinfo is a dict
            if type(modinfo) is dict:
                modinfo = [modinfo]

            for eachmodinfo in modinfo:
                modnumkey = get_key(modulekeys.MOD_NUM, self._SW_VER)
                m = Module(self, eachmodinfo[modnumkey], eachmodinfo)
                mret[int(eachmodinfo[modnumkey])] = m
        return mret

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
