# All common constants for the lib can be put here

DEFAULT = "DEFAULT"

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
