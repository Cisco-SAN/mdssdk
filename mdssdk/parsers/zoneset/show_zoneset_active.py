import logging
import re

log = logging.getLogger(__name__)

PAT_NAME = "zoneset name\s+(?P<name>\S+)\s+vsan\s+(?P<vsan>\d+)"


class ShowZonesetActive(object):
    def __init__(self, outlines):
        self._name = {}
        self.process_all(outlines)
        log.debug(self._name)

    def process_all(self, outlines):
        match = re.search(PAT_NAME, outlines[0])
        if match:
            self._name = match.groupdict()

    @property
    def active(self):
        return self._name.get("name", None)
