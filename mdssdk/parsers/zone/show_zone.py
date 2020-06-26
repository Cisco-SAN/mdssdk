import logging
import re

log = logging.getLogger(__name__)

PAT_ZONE = "zone name\s+(?P<name>\S+)\s+vsan\s+(?P<vsan>\d+)"
PAT_PWWN = "pwwn\s+(?P<pwwn>[0-9a-f:]+).*"
PAT_FWWN = "fwwn\s+(?P<fwwn>[0-9a-f:]+).*"
PAT_FCID = "fcid\s+(?P<fcid>\S+)"
PAT_PORT_CH = "interface\s+port-channel\s(?P<interface>\d+)"
PAT_FC = "interface\s(?P<interface>fc\d+\/\d+)"
PAT_FCALIAS = "fcalias name\s+(?P<fcalias>\S+)"
PAT_IP = "ip-address\s+(?P<ipaddress>\S+)"
PAT_SYM = "symbolic-nodename\s+(?P<symbolicnodename>\S+)"
PAT_MEMBERS = [
    PAT_PWWN,
    PAT_FWWN,
    PAT_FCID,
    PAT_FCALIAS,
    PAT_PORT_CH,
    PAT_FC,
    PAT_IP,
    PAT_SYM,
]


class ShowZone(object):
    def __init__(self, outlines):
        self._name = {}
        self._members = []
        self.process_all(outlines)
        log.debug(self._name)
        log.debug(self._members)

    def process_all(self, outlines):
        match = re.search(PAT_ZONE, outlines[0])
        if match:
            self._name = match.groupdict()
        for line in outlines:
            line = line.strip()
            for pat in PAT_MEMBERS:
                match = re.search(pat, line)
                if match:
                    mem = match.groupdict()
                    if pat == PAT_SYM:
                        mem = {"symbolic-nodename": mem["symbolicnodename"]}
                    elif pat == PAT_IP:
                        mem = {"ip-address": mem["ipaddress"]}
                    elif pat == PAT_PORT_CH:
                        mem = {"interface": int(mem["interface"])}
                    self._members.append(mem)

    @property
    def name(self):
        return self._name.get("name", None)

    @property
    def members(self):
        if not self._members:
            return None
        return self._members
