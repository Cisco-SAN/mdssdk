from ..constants import DEFAULT

# ------------------------------------ #
# show device-alias status
# ------------------------------------ #
# "fabric_distribution": "Enabled",
# "database_device_aliases": "3845",
# "database_mode": "Enhanced",
# "database_checksum": "0xeaa2372089608e3db918d76d9cc1cf3",
# "Locked_by_user": "CLI/SNMPv3:admin",
# "Locked_by_SWWN": "20:00:00:de:fb:b1:8e:b0",
# "pending_database_device_aliases": "3844",
# "pending_database_mode": "Enhanced"
FABRIC_DISTRIBUTE = {
    DEFAULT: "fabric_distribution",
    "8.4(0)": "dummy_distribution",
    "8.4(2)": "some_other_key_names",
}
MODE = {DEFAULT: "database_mode"}
NUM_DA = {DEFAULT: "database_device_aliases"}
LOCKED_USER = {DEFAULT: "Locked_by_user"}
LOCKED_SWWN = {DEFAULT: "Locked_by_SWWN"}
