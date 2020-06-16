import logging
import re

log = logging.getLogger(__name__)

PAT_FC_BR = "(?P<interface>fc\d+\/\d+)\s+(?P<vsan>\d+)\s+(?P<admin_mode>\S+)\s+(?P<admin_trunk_mode>\S+)\s+(?P<status>\S+)\s+(?P<fcot_info>\S+)\s+(?P<oper_mode>\S+)\s+(?P<oper_speed>\S+)\s+(?P<port_channel>\S+)\s+(?P<logical_type>\S+)"
PAT_PC_BR = "(?P<interface>port-channel\d+)\s+(?P<vsan>\d+)\s+(?P<admin_trunk_mode>\S+)\s+(?P<status>\S+)\s+(?P<oper_mode>\S+)\s+(?P<oper_speed>\S+)\s+(?P<ip_address>\S+)\s+(?P<logical_type>\S+)"
PAT_FC = "^fc\d+\/\d+$"
PAT_PC = "^port-channel\d+$"


class ShowInterfaceBrief(object):
    def __init__(self, outlines, name=None):
        self._fc_interfaces = []
        self._pc_interfaces = []
        self._group_dict = {}
        self.name = name
        self.process_all(outlines)
        log.debug(self._fc_interfaces)
        log.debug(self._pc_interfaces)
        log.debug(self._group_dict)

    def process_all(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match_fc_br = re.finditer(PAT_FC_BR, outlines)
        if match_fc_br:
            self._fc_interfaces = [m.groupdict() for m in match_fc_br]
        match_pc_br = re.finditer(PAT_PC_BR, outlines)
        if match_pc_br:
            self._pc_interfaces = [m.groupdict() for m in match_pc_br]
        if self.name is not None:
            fcmatch = re.match(PAT_FC, self.name)
            pcmatch = re.match(PAT_PC, self.name)
            if fcmatch:
                self._group_dict = next(
                    (
                        i
                        for i in self._fc_interfaces
                        if i["interface"] == str(self.name)
                    ),
                    {},
                )
            elif pcmatch:
                self._group_dict = next(
                    (
                        i
                        for i in self._pc_interfaces
                        if i["interface"] == str(self.name)
                    ),
                    {},
                )

    @property
    def mode(self):
        return self._group_dict.get("oper_mode", None)

    @property
    def speed(self):
        return self._group_dict.get("oper_speed", None)

    @property
    def trunk(self):
        return self._group_dict.get("admin_trunk_mode", None)

    @property
    def status(self):
        return self._group_dict.get("status", None)

    @property
    def interfaces(self):
        allfc = [fc["interface"] for fc in self._fc_interfaces]
        allpc = [pc["interface"] for pc in self._pc_interfaces]
        return allfc, allpc
