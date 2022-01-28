import logging

log = logging.getLogger(__name__)


class Fdmi:
    """
    Fdmi Module

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
        >>> fdmi_hand = Fdmi(sw)
        >>> print(fdmi_hand)
        <mdssdk.fdmi.Fdmi object at 0x103fd5e10>

    """

    def __init__(self, switch, hbaid=None, vsan=None):
        ERR1 = "ERROR!!! vsan argument cant be empty while passing hbaid argument. Please pass both hbaid and vsan or only vsan"
        self._sw = switch
        self._hbaid = hbaid
        self._vsan = vsan
        self._alldata = []
        if self._hbaid is None:
            if self._vsan is None:
                cmd = "show fdmi database detail"
            else:
                cmd = "show fdmi database detail vsan " + str(self._vsan)
        else:
            if self._vsan is None:
                print(ERR1)
                exit()
            else:
                cmd = "show fdmi database detail hba-id " + self._hbaid + " vsan " + str(self._vsan)
        out = self._sw.show(cmd)
        if self._sw.is_connection_type_ssh():
            self._alldata = out
        else:
            if out:
                reqout = out["TABLE_vsan"]["ROW_vsan"]
                if type(reqout) is dict:
                    all_reqout = [reqout]
                else:
                    all_reqout = reqout
                for reqout in all_reqout:
                    vk = "vsan"
                    vsan = reqout[vk]
                    hbadata = reqout["TABLE_hba_id"]["ROW_hba_id"]
                    for each_hbadata in hbadata:
                        piddata = each_hbadata.get("TABLE_port_id", {})
                        # print(piddata)
                        if piddata:
                            reqpiddata = piddata["ROW_port_id"][0]
                            each_hbadata.pop("TABLE_port_id")
                            tmp = {}
                            tmp[vk] = vsan
                            newdict = {**tmp, **each_hbadata, **reqpiddata}
                            self._alldata.append(newdict)
        # print(self._alldata)

    def hbas(self, vsan=None):
        """
        Returns all the hba's that are registered

        :param vsan: vsan list for which hba list needs to be fetched (optional)
        :type vsan: list
        :return: Returns all the hba's that are registered
        :rtype: dict(vsan:hba list)
        :example:
            >>> allhbas = fdmi.hbas()
            >>> print(allhbas)
            {1: ['10:00:00:10:9b:95:41:9c', '20:05:00:11:0d:fd:4f:00'],
             167: ['20:02:00:11:0d:5a:35:00',
                   '20:03:00:11:0d:5a:36:00',
                   '20:07:00:11:0d:60:01:00']}
            >>>
        """
        retdict = {}
        for eachele in self._alldata:
            v = eachele['vsan']
            hba = eachele['hba']
            tmplist = retdict.get(v, [])
            tmplist.append(hba)
            retdict[v] = tmplist
        if vsan is None:
            return retdict
        else:
            if type(vsan) is not list:
                raise TypeError("vsan argument has to be of type list")
            tmpdict = {v: retdict[v] for v in vsan if v in retdict}
            return tmpdict

    def database_detail(self, vsan=None, hbaid=None):
        """
        Returns all the hba details registered in a dict format

        :param vsan: vsan list for which details needs to be fetched (optional)
        :type vsan: list
        :param hbaid: hbaid list for which details needs to be fetched (optional)
        :type hbaid: list
        :return: Returns all the hba's discovered
        :rtype: dict(vsan:hba details)
        :example:
            >>> allhbas = fdmi.database_detail()
            >>> print(allhbas)
            {1: [{'current_speed': '32G',
              'driver_ver': '8.07.00.34.Trunk-SCST.18-k',
              'firmware_ver': '8.08.204 (785ad0ult',
              'hardware_ver': 'BK3210407-43 02',
              'hba': '20:05:00:11:0d:fd:4f:00',
              'host_name': 'VirtuaLUN',
              'manufacturer': 'QLogic Corporation',
              'maximum_frame_size': 2112,
              'model': 'QLE2742',
              'model_description': 'Cisco QLE2742 Dual Port 32Gb FC to PCIe Gen3 x8 '
                                   'Adapter',
              'node_name': '20:05:00:11:0d:fd:4f:00',
              'os_device_name': 'qla2xxx:host14',
              'port': '20:05:00:11:0d:fd:4f:00',
              'rom_ver': '3.39',
              'serial_num': 'RFD1610K18684',
              'supported_fc4_types': ['scsi-fcp', 'NVMe', 'fc-av'],
              'supported_speeds': ['8G', '16G', '32G']}]}
                                   '20:07:00:11:0d:60:01:00']}
            >>>
        """
        if vsan is None and hbaid is None:
            retdict = {}
            for eachele in self._alldata:
                v = eachele['vsan']
                tmplist = retdict.get(v, [])
                del eachele['vsan']
                tmplist.append(eachele)
                retdict[v] = tmplist
            return retdict
        elif vsan is None:
            if type(hbaid) is not list:
                raise TypeError("hbaid argument has to be of type list")
            retdict = {}
            for eachele in self._alldata:
                v = eachele['vsan']
                hba = eachele['hba']
                if hba not in hbaid:
                    continue
                tmplist = retdict.get(v, [])
                del eachele['vsan']
                tmplist.append(eachele)
                retdict[v] = tmplist
            return retdict
        elif hbaid is None:
            if type(vsan) is not list:
                raise TypeError("vsan argument has to be of type list")
            retdict = {}
            for eachele in self._alldata:
                v = eachele['vsan']
                if v not in vsan:
                    continue
                tmplist = retdict.get(v, [])
                del eachele['vsan']
                tmplist.append(eachele)
                retdict[v] = tmplist
            return retdict
        else:
            raise TypeError("Either of vsan or hbaid argument needs to be passed, not both ")
