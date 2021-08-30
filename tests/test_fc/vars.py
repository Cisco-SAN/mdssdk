import logging

log = logging.getLogger(__name__)

ANA_SUPP_MOD = [
    "DS-X9648-1536K9",
    "DS-C9132T-K9-SUP",
    "DS-C9132U-K9-SUP",
    "DS-C9148T-K9-SUP",
    "DS-C9396T-K9-SUP",
]
analytics_values = ["scsi", "nvme", "all", None]

trunk_values = ["on", "off", "auto"]

mode_values = ["E", "F", "Fx", "NP", "SD", "auto"]

speed_values_read = ["1", "2", "4", "8", "16", "32", "--"]
speed_values_write = [1000, 2000, 4000, 8000, 16000, "auto"]

status_values = [
    "inactive",
    "notConnected",
    "errDisabled",
    "up",
    "down",
    "sfpAbsent",
    "trunking",
    "channelDown",
    "outofServc",
    "isolated",
    "licenseNotAvail",
    "init",
    "offline",
]


def get_mod_port(fcport):
    mod = fcport.split("/")[0].lstrip("fc")
    port = fcport.split("/")[1]
    return int(mod), int(port)
