import json
import logging
import random

from mdssdk.switch import Switch

logging.basicConfig(filename='test_zone.log', filemode='w', level=logging.INFO,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

def get_random_id(start=2, end=400):
    return random.randint(start, end)

members_dict = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
                {'ip-address': '1.1.1.1'},
                {'fwwn': '11:12:13:14:15:16:17:18'},
                {'fcid': '0x123456'},
                {'symbolic-nodename': 'testsymnode'}]