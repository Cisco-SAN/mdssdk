import logging
import re

from ..constants import PAT_WWN

log = logging.getLogger()


def is_pwwn_valid(pwwn):
    newpwwn = pwwn.lower()
    match = re.match(PAT_WWN, newpwwn)
    if match:
        return True
    return False


def get_key(nxapikey, version=None):
    if version in nxapikey.keys():
        return nxapikey[version]
    else:
        return nxapikey['DEFAULT']
