import logging
import re

log = logging.getLogger(__name__)


class ShowVsanMembership(object):
    def __init__(self, outlines):
        self._interfaces = []
        self.process(outlines)
        log.debug(self._interfaces)

    def process(self, outlines):
        PAT = "interfaces:\s+(?P<interfaces>.*)"
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match = re.findall(PAT, outlines)
        if match:
            self._interfaces = match[0].split()
        else:
            self._interfaces = None

    @property
    def interfaces(self):
        return self._interfaces
