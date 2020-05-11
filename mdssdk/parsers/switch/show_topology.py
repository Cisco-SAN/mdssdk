__author__ = 'Suhas Bharadwaj (subharad)'

import re


class ShowTopology(object):
    def __init__(self, cmdoutput):
        self.__alloutput = cmdoutput
        self.__pat_for_vsan = "^FC Topology for VSAN ([0-9]+) :"
        self.__pat_for_value_line = "\s+(\S+)\s+(0x[0-9a-f]+)\S+\s+(\S+)\s+(\d+\.\d+\.\d+\.\d+)"

        # Stored format is
        # {'vsan':((local_int,peer_dom,peer_int,peer_ip),(local_int,peer_dom,peer_int,peer_ip),'vsan':((local_int,peer_dom,peer_int,peer_ip),(local_int,peer_dom,peer_int,peer_ip))
        # Example is
        # {'10': (('port-channel3', '0xab', 'port-channel3', '10.126.94.110'), ('port-channel7', '0x26', 'port-channel9', '10.126.94.103'), ('port-channel8', '0x26', 'port-channel10', ......
        self.parse_data = {}

        # Call function to parse the output
        # self.__process_output()
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
                    self.parse_data[vsan] = intlist
                    intlist = []
                vsan = matchvsan.group('vsan')

            matchint = re.search(int_regex, line)
            if matchint:
                dummy = {}
                dummy['interface'] = matchint.group('interface')
                dummy['peer_domain'] = matchint.group('peer_domain')
                dummy['peer_interface'] = matchint.group('peer_interface')
                dummy['peer_ip'] = matchint.group('peer_ip')
                dummy['peer_switch_name'] = matchint.group('peer_switch_name')
                intlist.append(dummy)
        # print(self.parse_data)

    def __process_output(self):
        # print("Processing ...")
        vsan = ""
        val = []
        for line in self.__alloutput:
            matchvsan = re.match(self.__pat_for_vsan, line)
            if matchvsan:
                if vsan != "" and val.__len__() != 0:
                    self.__data[vsan] = tuple(val)
                    val = []
                vsan = matchvsan.group(1)
            # print(vsan)
            matchval = re.match(self.__pat_for_value_line, line)
            # print(matchval)
            if matchval:
                local_int = matchval.group(1)
                peer_dom = matchval.group(2)
                peer_int = matchval.group(3)
                peer_ip = matchval.group(4)
                v = (local_int, peer_dom, peer_int, peer_ip)
                val.append(v)
        if vsan != "" and val.__len__() != 0:
            self.__data[vsan] = tuple(val)

    def get_all_data(self):
        return self.__data

    def get_topo_per_vsan(self, vsan):
        return self.__data[str(vsan)]

    def get_all_peer_ip_addrs(self):
        peer_ip_list = []
        for key, val in self.__data.iteritems():
            [peer_ip_list.append(v[3]) for v in val]

        return list(set(peer_ip_list))

    def get_connected_links(self):
        peer_list = []
        for key, val in self.__data.iteritems():
            for v in val:
                peer_list.append([v[0], v[2], v[3]])

        return peer_list
