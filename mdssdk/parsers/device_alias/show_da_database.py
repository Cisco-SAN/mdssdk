import logging
import re

log = logging.getLogger(__name__)


class ShowDeviceAliasDatabase(object):
    def __init__(self, outlines):
        self._da_pwwn = {}
        self.process(outlines)

    def process(self, outlines):
        PAT = "device-alias name\s+(\S+)\s+pwwn\s+(\S+)"
        for eachline in outlines:
            eachline = eachline.strip().strip("\n")
            regex = re.compile(PAT)
            match = regex.match(eachline)
            if match:
                self._da_pwwn[match.group(1)] = match.group(2)
        log.debug(self._da_pwwn)

    @property
    def database(self):
        if self._da_pwwn:
            return self._da_pwwn
        return None
