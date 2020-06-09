import logging
import re

log = logging.getLogger(__name__)


class ShowPortChannelDatabase(object):
    def __init__(self, outlines, pc_id=None):
        self._pc_db = []
        self._pc_id = pc_id
        self.process(outlines)
        log.debug(self._pc_db)

    def process(self, outlines):
        PAT = "port-channel(?P<interface>\d+)"
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match = re.finditer(PAT, outlines)
        if match:
            self._pc_db = [m.groupdict() for m in match]

    @property
    def present(self):
        pc = next((pc for pc in self._pc_db if pc["interface"] == str(self._pc_id)), {})
        if pc:
            return True
        return False
