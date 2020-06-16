import logging
import re

log = logging.getLogger(__name__)


class ShowInterfaceDescription(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process_all(outlines)

    def process_all(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        PAT_DESC = "(port-channel\d+|fc\d+\/\d+)\s+(?P<description>\S+)"
        match = re.search(PAT_DESC, outlines)
        if match:
            self._group_dict = match.groupdict()
            log.debug(self._group_dict)

    @property
    def description(self):
        return self._group_dict.get("description", None)
