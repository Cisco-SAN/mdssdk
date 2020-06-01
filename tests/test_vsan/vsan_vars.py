import json
import logging
import random

from mdssdk.switch import Switch

logging.basicConfig(filename='test_vsan.log', filemode='w', level=logging.INFO,
					format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

reserved_id = [4079, 4094]
boundary_id = [0, 4095]


# No need to have end=4094 as there are some inbetween vsans reserved for fport-channel-trunk
def get_random_id(start=2, end=400):
    return random.randint(start, end)
