import json
import logging

from mdssdk.switch import Switch

logging.basicConfig(filename='test_switch.log', filemode='w', level=logging.INFO,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

ip_address = data['ip_address']
