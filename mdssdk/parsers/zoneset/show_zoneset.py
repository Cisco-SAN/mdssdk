import logging
import re

log = logging.getLogger(__name__)

PAT_NAME = "zoneset name\s+(?P<name>\S+)\s+vsan\s+(?P<vsan>\d+)"
PAT_MEMBERS = "zone name\s+(?P<name>\S+)\s+vsan\s+(?P<vsan>\d+)"


class ShowZoneset(object):
    def __init__(self, outlines):
        self._name = {}
        self._members = []
        self.process_all(outlines)
        log.debug(self._name)
        log.debug(self._members)

    def process_all(self, outlines):
        match = re.search(PAT_NAME, outlines[0])
        if match:
            self._name = match.groupdict()
        for line in outlines:
            line = line.strip()
            match = re.search(PAT_MEMBERS, line)
            if match:
                mem = match.groupdict()
                self._members.append(mem)

    @property
    def name(self):
        return self._name.get("name", None)

    @property
    def members(self):
        if not self._members:
            return None
        return self._members
