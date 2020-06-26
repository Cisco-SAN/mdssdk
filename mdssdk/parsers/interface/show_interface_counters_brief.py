import logging
import re

log = logging.getLogger(__name__)

PAT = "(?P<interface>(port-channel\d+|fc\d+\/\d+))\s+(?P<input_rate>\d+)\s+(?P<frames_in>\d+)\s+(?P<output_rate>\d+)\s+(?P<frames_out>\d+)"


class ShowInterfaceCountersBrief(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process_all(outlines)
        log.debug(self._group_dict)

    def process_all(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        match = re.search(PAT, outlines)
        if match:
            self._group_dict = match.groupdict()

    @property
    def brief(self):
        return self._group_dict
