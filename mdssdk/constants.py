# All common constants for the lib can be put here

DEFAULT = "DEFAULT"

# Supported connection types
VALID_CONN_TYPES = ["https", "http", "ssh"]

# Supported switch PIDs
VALID_PIDS_MDS = ("DS-", "89")
VALID_PIDS_FI = "UCS-FI"
VALID_PIDS_N9K = "N9K"

# Timeouts in secs
SSH_CONN_TIMEOUT = 100
NXAPI_CONN_TIMEOUT = 100
CLI_CMD_TIMEOUT = 100
RELOAD_TIMEOUT = 300
ISSU_TIMEOUT = 1800

# DEF PORTS
HTTPS_PORT = 8443
HTTP_PORT = 8080

# Patterns
PAT_FC = "^fc([1-9][0-9]?)/([1-9][0-9]?)$"
PAT_PC = "^port-channel([1-9][0-9]?[0-9]?)$"
PAT_FCIP = "fcip([0-9]+)"
PAT_WWN = "([0-9,a-f]{1,2}:){7}[0-9,a-f]{1,2}"

# Interface trunk and state related
ON = "on"
OFF = "off"
AUTO = "auto"
SHUTDOWN = "shutdown"
NO_SHUTDOWN = "no shutdown"
OUT_OF_SERVICE = "outOfServc"
MODE_E = "E"
MODE_F = "F"
MODE_NP = "NP"
VALID_STATUS = [SHUTDOWN, NO_SHUTDOWN]
VALID_TRUNK_MODE = [AUTO, ON, OFF]
VALID_SPEED = [AUTO, 1000, 2000, 4000, 8000, 16000, 32000]
VALID_MODE = [AUTO, MODE_E, MODE_F, MODE_NP]

# PC related
ACTIVE = "active"
VALID_PC_RANGE = range(1, 257)  # 1-256

# Vsan related
VALID_VSAN = range(1, 4095)  # 1-4094
RESERVED_VSAN = [1, 4079, 4094]
SUSPEND = "suspend"
NO_SUSPEND = "no suspend"

# Zone related
BASIC = "basic"
ENHANCED = "enhanced"
PERMIT = "permit"
DENY = "deny"

# FCIP related
VALID_FCIP_RANGE = range(1, 513)  # 1-512
VALID_FCIP_PROFILE_RANGE = range(1, 513)  # 1-512
