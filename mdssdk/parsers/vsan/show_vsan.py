import logging
import re

log = logging.getLogger(__name__)


class ShowVsan(object):
    def __init__(self, outlines, vsan_id=None):
        self._all_vsans = []
        self._group_dict = {}
        self.vsan_id = vsan_id
        self.process_all(outlines)

    def process_all(self, outlines):
        outlines = "".join([eachline.strip("\n") for eachline in outlines])
        PAT_VSAN_INFO = "vsan\s(?P<vsan>\d*)(\sinformation\s+name:(?P<name>\S*)\s+state:(?P<state>\S*)\s+interoperability mode:(?P<interop_mode>\S*)\s+loadbalancing:(?P<load_balancing>\S*)\s+operational state:(?P<operational_state>\S*))?"
        regex = re.compile(PAT_VSAN_INFO)
        match = regex.finditer(outlines)
        if match:
            self._all_vsans = [m.groupdict() for m in match]
            self._group_dict = next(
                (v for v in self._all_vsans if v["vsan"] == str(self.vsan_id)), {}
            )
            log.debug(self._all_vsans)
            log.debug(self._group_dict)

    @property
    def id(self):
        vsan_id = self._group_dict.get("vsan", None)
        if vsan_id is not None:
            return int(vsan_id)
        return None

    @property
    def name(self):
        return self._group_dict.get("name", None)

    @property
    def state(self):
        return self._group_dict.get("state", None)

    @property
    def interop_mode(self):
        return self._group_dict.get("interop_mode", None)

    @property
    def load_balancing(self):
        return self._group_dict.get("load_balancing", None)

    @property
    def operational_state(self):
        return self._group_dict.get("operational_state", None)

    @property
    def vsans(self):
        return self._all_vsans
