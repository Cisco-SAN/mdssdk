__author__ = "Suhas Bharadwaj (subharad)"

import re


class ShowFcsIe(object):
    def __init__(self, cmdoutput):
        self.__alloutput = cmdoutput
        # IE List for VSAN: 1
        self.__pat_for_vsan = "^IE List for VSAN:(?P<vsan>\d+)"
        # 20:01:00:2a:6a:1b:5f:31  S(Rem) 0xfffcee 10.126.94.108 (sw108-9250i)
        self.__pat_for_value_line = "(?P<wwn>([0-9a-f]+:){7}[0-9a-f]+)\s+(?P<ie>\S+)\((?P<ie_status>\S+)\)\s+(?P<mgmt_id>0x[0-9a-f]+)\s+(?P<mgmt_ip>\S+)\s+\((?P<switch_name>\S+)\)"
        self._parse_data = {}

        # Call function to parse the output
        self.__parse()

    def __parse(self):
        vallist = []
        for line in self.__alloutput:
            matchvsan = re.search(self.__pat_for_vsan, line)
            if matchvsan:
                if vsan is not None:
                    self._parse_data[vsan] = vallist
                    vallist = []
                vsan = matchvsan.group("vsan")
                # print(vsan)

            matchval = re.search(self.__pat_for_value_line, line)
            if matchval:
                dummy = {}
                dummy["wwn"] = matchval.group("wwn")
                dummy["ie"] = matchval.group("ie")
                dummy["ie_status"] = matchval.group("ie_status")
                dummy["mgmt_id"] = matchval.group("mgmt_id")
                dummy["mgmt_ip"] = matchval.group("mgmt_ip")
                dummy["switch_name"] = matchval.group("switch_name")
                vallist.append(dummy)
        if vsan is not None:
            self._parse_data[vsan] = vallist
        # print(self._parse_data)

    def get_all_data(self):
        return self._parse_data

    def get_data_per_vsan(self, vsan):
        return self._parse_data[str(vsan)]
