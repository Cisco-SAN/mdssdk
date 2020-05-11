import logging
import re

log = logging.getLogger(__name__)

PAT_VER = "system:    version\s+(?P<version>\S+).*"
PAT_KICK = "kickstart image file is:\s+(?P<kickstart_image>.*)"
PAT_SYS = "system image file is:\s+(?P<system_image>.*)"
PAT_MODEL = "cisco\s+(?P<model>.*Chassis).*"
ALL_PATS = [
    PAT_VER,
    PAT_KICK,
    PAT_SYS,
    PAT_MODEL
]


class ShowVersion(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process_all(outlines)
        log.debug(self._group_dict)

    def process_all(self, outlines):
        for eachline in outlines:
            eachline = eachline.strip().strip("\n")
            for eachpat in ALL_PATS:
                regex = re.compile(eachpat)
                match = regex.match(eachline)
                if match:
                    self._group_dict = {**self._group_dict, **match.groupdict()}
                    break
        log.debug(self._group_dict)

    @property
    def version(self):
        return self._group_dict.get('version', None)

    @property
    def kickstart_image(self):
        return self._group_dict.get('kickstart_image', None)

    @property
    def system_image(self):
        return self._group_dict.get('system_image', None)

    @property
    def model(self):
        return self._group_dict.get('model', None)
