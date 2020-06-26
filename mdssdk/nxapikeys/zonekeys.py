from ..constants import DEFAULT

# This file contains NXAPI keys for zone and zoneset

# Valid zone members
VALID_MEMBERS = {
    DEFAULT: {
        "pwwn": "wwn",
        "interface": "intf",
        "device-alias": "dev_alias",
        "ip-address": "ipaddr",
        "symbolic-nodename": "symnodename",
        "fwwn": "wwn",
        "fcid": "fcid",
        "fcalias": "fcalias_name",
    },
    "SSH": {
        "pwwn": "pwwn",
        "interface": "interface",
        "device-alias": "device_alias",
        "ip-address": "ip_address",
        "symbolic-nodename": "symbolic_nodename",
        "fwwn": "fwwn",
        "fcid": "fcid",
        "fcalias": "fcalias",
    },
}

# --------------------- #
# show zone status vsan <>
# --------------------- #
# show zone name vsan <>
# --------------------- #
# show zoneset name vsan <>
# --------------------- #

NAME = {DEFAULT: "name"}
VSAN_ID = {DEFAULT: "vsan", "8.4(2a)": "vsan"}
DEFAULT_ZONE = {DEFAULT: "default_zone"}
DISTRIBUTE = {DEFAULT: "distribute"}
INTEROP = {DEFAULT: "interop"}
MODE = {DEFAULT: "mode"}
MERGE_CONTROL = {DEFAULT: "merge_control"}
SESSION = {DEFAULT: "session"}
SMART_ZONE = {DEFAULT: "smart_zoning"}
ZONE_DETAILS = {DEFAULT: "zone_details"}
FULLDB_SIZE = {DEFAULT: "fulldb_dbsize"}
FULLDB_ZSC = {DEFAULT: "fulldb_zoneset_count"}
FULLDB_ZC = {DEFAULT: "fulldb_zone_count"}
ACTIVEDB_SIZE = {DEFAULT: "activedb_dbsize"}
ACTIVEDB_ZSN = {DEFAULT: "activedb_zoneset_name"}
ACTIVEDB_ZSC = {DEFAULT: "activedb_zoneset_count"}
ACTIVEDB_ZC = {DEFAULT: "activedb_zone_count"}
EFFDB_SIZE = {DEFAULT: "effectivedb_dbsize"}
MAXDB_SIZE = {DEFAULT: "maxdb_dbsize"}
EFFDB_PER = {DEFAULT: "percent_effectivedbsize"}
STATUS = {DEFAULT: "status"}

# ZONE_MEMBERS = ['TABLE_zone_member']['ROW_zone_member']
ZONE_MEMBER_TYPE = {DEFAULT: "type"}
ZONE_MEMBER_WWN = {DEFAULT: "wwn"}
ZONE_MEMBER_INTERFACE = {DEFAULT: "intf_fc"}
ZONE_MEMBER_DEVALIAS = {DEFAULT: "dev_alias"}
ZONE_MEMBER_IPADDR = {DEFAULT: "ipaddr"}
ZONE_MEMBER_SYMNODENAME = {DEFAULT: "symnodename"}
ZONE_MEMBER_FWWN = {DEFAULT: "wwn"}
ZONE_MEMBER_SWWN = {DEFAULT: "wwn"}
ZONE_MEMBER_FCID = {DEFAULT: "fcid"}
ZONE_MEMBER_INTERFACE_PC = {DEFAULT: "intf_port_ch"}
ZONE_MEMBER_FCALIAS = {DEFAULT: "fcalias_name"}
ZONE_MEMBER_FCALIAS_VSANID = {DEFAULT: "fcalias_vsan_id"}
