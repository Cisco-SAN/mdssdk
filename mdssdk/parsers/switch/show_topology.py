__author__ = "Suhas Bharadwaj (subharad)"

import re


class ShowTopology(object):
    def __init__(self, cmdoutput):
        self.__alloutput = cmdoutput
        self.__pat_for_vsan = "^FC Topology for VSAN ([0-9]+) :"
        self.__pat_for_value_line = (
            "\s+(\S+)\s+(0x[0-9a-f]+)\S+\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)"
        )

        # Stored format is
        # {'1': [{'interface': 'fc2/43', 'peer_domain': '0xdc', 'peer_interface': 'fc1/12', 'peer_ip_address': '10.126.94.220', 'peer_switch_name': 'sw220-L13-Ishan'},
        # {'interface': 'fc13/1', 'peer_domain': '0xe8', 'peer_interface': 'fc1/48', 'peer_ip_address': '10.126.94.129', 'peer_switch_name': 'sw129-Luke'},
        # {'interface': 'fc13/3', 'peer_domain': '0xe5', 'peer_interface': 'fc6/31', 'peer_ip_address': '10.126.94.184', 'peer_switch_name': 'sw184-9706'},
        # {'interface': 'fc13/4', 'peer_domain': '0xc7', 'peer_interface': 'fc1/15', 'peer_ip_address': '10.126.94.217', 'peer_switch_name': 'sw217-Ishan-L13-withLem'},...
        self._parse_data = {}

        # Call function to parse the output
        self.__parse()

    def __parse(self):
        intlist = []
        vsan = None
        van_regex = "^FC Topology for VSAN\s+(?P<vsan>\d+).*"
        int_regex = "\s+(?P<interface>\S+)\s+(?P<peer_domain>0x[0-9a-f]+)\S+\s+(?P<peer_interface>\S+)\s+(?P<peer_ip>\d+\.\d+\.\d+\.\d+)\((?P<peer_switch_name>\S+)\)"

        for line in self.__alloutput:
            matchvsan = re.search(van_regex, line)
            if matchvsan:
                if vsan is not None:
                    self._parse_data[vsan] = intlist
                    intlist = []
                vsan = matchvsan.group("vsan")
                # print(vsan)

            matchint = re.search(int_regex, line)
            if matchint:
                dummy = {}
                dummy["interface"] = matchint.group("interface")
                dummy["peer_domain"] = matchint.group("peer_domain")
                dummy["peer_interface"] = matchint.group("peer_interface")
                dummy["peer_ip_address"] = matchint.group("peer_ip")
                dummy["peer_switch_name"] = matchint.group("peer_switch_name")
                intlist.append(dummy)
                # print(intlist)
        if vsan is not None:
            self._parse_data[vsan] = intlist
        # print(self._parse_data)

    def get_all_data(self):
        return self._parse_data

    def get_topo_per_vsan(self, vsan):
        return self._parse_data[str(vsan)]

    def get_all_peer_ip_addrs(self):
        peer_ip_list = []
        for key, val in self._parse_data.items():
            [peer_ip_list.append(v["peer_ip_address"]) for v in val]
        return list(set(peer_ip_list))
