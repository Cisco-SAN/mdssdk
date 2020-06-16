import logging
import re

log = logging.getLogger(__name__)

PAT_LOCK = "session:\s+(?P<locked>\S+)"
PAT_MODE = "mode:\s+(?P<mode>\S+)"
PAT_DEFAULT = "default-zone:\s+(?P<default_zone>\S+)"
PAT_SMART = "smart-zoning:\s+(?P<smart_zone>\S+)"
PAT_FULL_DB = "Full Zoning Database :\s+DB size:\s+(?P<fulldb_size>\d+)\s+bytes\s+Zonesets:\s+(?P<fulldb_zoneset_count>\d+)\s+Zones:\s+(?P<fulldb_zone_count>\d+)"
PAT_EFF_DB = "Current Total Zone DB Usage:\s+(?P<effectivedb_size>\d+)\s+\/\s+(?P<maxdb_size>\d+)\s+bytes\s+\((?P<effectivedb_size_percentage>\d+)"
PAT_ACTIVE_DB = "Active Zoning Database :\s+DB Size:\s+(?P<activedb_size>\d+)\s+bytes\s+Name:\s+(?P<activedb_zoneset_name>\S+)\s+Zonesets:\s+(?P<activedb_zoneset_count>\d+)\s+Zones:\s+(?P<activedb_zone_count>\d+)"
PAT_STATUS = "Status:\s+(?P<status>.*)"
ALL_PAT = [
    PAT_LOCK,
    PAT_MODE,
    PAT_DEFAULT,
    PAT_SMART,
    PAT_FULL_DB,
    PAT_EFF_DB,
    PAT_ACTIVE_DB,
    PAT_STATUS,
]


class ShowZoneStatus(object):
    def __init__(self, outlines):
        self._group_dict = {}
        self.process_all(outlines)
        log.debug(self._group_dict)

    def process_all(self, outlines):
        outlines = "".join([eachline for eachline in outlines])
        for pat in ALL_PAT:
            match = re.search(pat, outlines)
            if match:
                mem = match.groupdict()
                self._group_dict.update(mem)

    @property
    def locked(self):
        return self._group_dict.get("locked", None)

    @property
    def mode(self):
        return self._group_dict.get("mode", None)

    @property
    def default_zone(self):
        return self._group_dict.get("default_zone", None)

    @property
    def smart_zone(self):
        return self._group_dict.get("smart_zone", None)

    @property
    def fulldb_size(self):
        return self._group_dict.get("fulldb_size", None)

    @property
    def fulldb_zone_count(self):
        return self._group_dict.get("fulldb_zone_count", None)

    @property
    def fulldb_zoneset_count(self):
        return self._group_dict.get("fulldb_zoneset_count", None)

    @property
    def activedb_size(self):
        return self._group_dict.get("activedb_size", None)

    @property
    def activedb_zone_count(self):
        return self._group_dict.get("activedb_zone_count", None)

    @property
    def activedb_zoneset_count(self):
        return self._group_dict.get("activedb_zoneset_count", None)

    @property
    def activedb_zoneset_name(self):
        return self._group_dict.get("activedb_zoneset_name", None)

    @property
    def maxdb_size(self):
        return self._group_dict.get("maxdb_size", None)

    @property
    def effectivedb_size(self):
        return self._group_dict.get("effectivedb_size", None)

    @property
    def effectivedb_size_percentage(self):
        return self._group_dict.get("effectivedb_size_percentage", None)

    @property
    def status(self):
        return self._group_dict.get("status", None)
