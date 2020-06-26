import logging
import re

log = logging.getLogger(__name__)

PAT = "(?P<interface>port-channel\d+)\s+Administrative channel mode is\s+(?P<admin_channel_mode>\S+)"
PAT_MEM = "(?P<port>fc\d+\/\d+)\s+(?P<channel_mode>\S+)\s+(?P<status>\S+)\s+(?P<mode>\S+)\s+(?P<local_wwn>\S+)\s+(?P<peer_wwn>\S+)\s+(?P<port_up_time>\S+)"


class ShowPortChannelDatabaseDetail(object):
    def __init__(self, outlines):
        self._pc_detail = {}
        self.process(outlines)
        log.debug(self._pc_detail)

    def process(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match = re.search(PAT, outlines)
        if match:
            self._pc_detail = match.groupdict()
            mem = re.finditer(PAT_MEM, outlines)
            if mem:
                self._pc_detail["members"] = [m.groupdict() for m in mem]

    @property
    def members(self):
        mem = self._pc_detail.get("members", None)
        if mem:
            return mem
        return None

    @property
    def admin_channel_mode(self):
        return self._pc_detail.get("admin_channel_mode", None)

    @property
    def channel_mode(self):
        if self.members:
            return self.members[0]["channel_mode"]
        return self.admin_channel_mode
