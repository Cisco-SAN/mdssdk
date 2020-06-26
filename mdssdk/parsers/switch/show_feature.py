import logging
import re

log = logging.getLogger(__name__)


class ShowFeature(object):
    def __init__(self, outlines):
        self._feature_list = {}
        self.process(outlines)

    def process(self, outlines):
        PAT = "(\S+)\s+\d+\s+(\S+)"
        for eachline in outlines:
            eachline = eachline.strip().strip("\n")
            regex = re.compile(PAT)
            match = regex.match(eachline)
            if match:
                self._feature_list[match.group(1)] = match.group(2)
        log.debug(self._feature_list)

    def is_enabled(self, feature):
        en_dis = self._feature_list.get(feature, None)
        if en_dis is not None:
            if en_dis == "enabled":
                return True
        return False
