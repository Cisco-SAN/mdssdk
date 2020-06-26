import logging
import re

log = logging.getLogger(__name__)

PAT_DIS = "Fabric Distribution :\s+(?P<distribute>.*)"
PAT_MODE = "Database:- Device Aliases.*Mode:\s+(?P<mode>.*)"
PAT_LOCKED = "Locked By:- User\s+(?P<locked_user>.*)\s+SWWN\s+(?P<locked_swwn>.*)"
ALL_PATS = [PAT_DIS, PAT_MODE, PAT_LOCKED]


class ShowDeviceAliasStatus(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process(outlines)

    def process(self, outlines):
        for eachline in outlines:
            eachline = eachline.strip().strip("\n")
            for eachpat in ALL_PATS:
                regex = re.compile(eachpat)
                match = regex.match(eachline)
                if match:
                    self._group_dict = {**self._group_dict, **match.groupdict()}
                    break

    @property
    def distribute(self):
        return self._group_dict.get("distribute", None)

    @property
    def mode(self):
        return self._group_dict.get("mode", None)

    @property
    def locked_user(self):
        return self._group_dict.get("locked_user", None)

    @property
    def locked_swwn(self):
        return self._group_dict.get("locked_swwn", None)
