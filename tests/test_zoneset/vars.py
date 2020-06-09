import json
import logging
import random

from mdssdk.switch import Switch

log = logging.getLogger(__name__)

with open('switch_details.json', 'r') as j:
    data = json.load(j)

log.info("Creating switch object")

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)


def get_random_id(start=2, end=400):
    return random.randint(start, end)


def get_random_pwwn():
    choicelist = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    entry = ""
    for i in range(16):
        e = random.choice(choicelist)
        entry = entry + e
        if i % 2 == 1:
            entry = entry + ":"
    return entry.rstrip(":")


members_dict = [{'pwwn': get_random_pwwn()},
                {'ip-address': '1.1.1.1'},
                {'fwwn': get_random_pwwn()},
                {'fcid': '0x123456'},
                {'symbolic-nodename': 'testsymnode'}]
