import logging
import re

log = logging.getLogger(__name__)

ALL_PAT = [
    "^fc\d+\/\d+\s+(?P<sfp_present>.*)",
    "Name is (?P<name>\S+)",
    "Manufacturer's part number is (?P<part_number>\S+)",
    "Cisco extended id is (?P<cisco_id>.*)",
    "Cisco part number is (?P<cisco_part_number>\S+)",
    "Cisco pid is (?P<cisco_product_id>\S+)",
    "Nominal bit rate is (?P<bit_rate>\d+)",
    "Min speed:\s+(?P<min_speed>\d+)\s+Mb/s,\s+Max speed:\s+(?P<max_speed>\d+)",
    "Temperature\s+(?P<temperature>\S+ C)",
    "Voltage\s+(?P<voltage>\S+ V)",
    "Current\s+(?P<current>\S+ mA)",
    "Tx Power\s+(?P<tx_power>\S+ dBm)",
    "Rx Power\s+(?P<rx_power>\S+ dBm)",
]


class ShowInterfaceTransceiverDetail(object):
    def __init__(self, outlines, vsan_id=None):
        self._group_dict = {}
        self.process_all(outlines)
        log.debug(self._group_dict)

    def process_all(self, outlines):
        for eachline in outlines:
            eachline = eachline.strip()
            for eachpat in ALL_PAT:
                match = re.search(eachpat, eachline)
                if match:
                    self._group_dict = {**self._group_dict, **match.groupdict()}
                    break

    @property
    def sfp_present(self):
        sfp = self._group_dict.get("sfp_present", None)
        if sfp is None:
            return None
        return "sfp is present" in sfp

    @property
    def name(self):
        return self._group_dict.get("name", None)

    @property
    def part_number(self):
        return self._group_dict.get("part_number", None)

    @property
    def cisco_id(self):
        return self._group_dict.get("cisco_id", None)

    @property
    def cisco_part_number(self):
        return self._group_dict.get("cisco_part_number", None)

    @property
    def cisco_product_id(self):
        return self._group_dict.get("cisco_product_id", None)

    @property
    def bit_rate(self):
        bit_rate = self._group_dict.get("bit_rate", None)
        if bit_rate is not None:
            return int(bit_rate)
        return None

    @property
    def min_speed(self):
        return self._group_dict.get("min_speed", None)

    @property
    def max_speed(self):
        return self._group_dict.get("max_speed", None)

    @property
    def temperature(self):
        return self._group_dict.get("temperature", None)

    @property
    def voltage(self):
        return self._group_dict.get("voltage", None)

    @property
    def current(self):
        return self._group_dict.get("current", None)

    @property
    def tx_power(self):
        return self._group_dict.get("tx_power", None)

    @property
    def rx_power(self):
        return self._group_dict.get("rx_power", None)
