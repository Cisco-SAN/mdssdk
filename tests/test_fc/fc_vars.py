import json
import logging
import random

from mdssdk.switch import Switch

logging.basicConfig(filename='test_fc.log', filemode='w', level=logging.INFO,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

analytics_values = ["scsi", "nvme", "all", None]

trunk_values = ['on', 'off', 'auto']

mode_values = ['E', 'F', 'Fx', 'NP', 'SD', 'auto']

speed_values_read = ['1', '2', '4', '8', '16', '32', '--']
speed_values_write = [1000, 2000, 4000, 8000, 16000, 'auto']

status_values = ["inactive", "notConnected", "errDisabled", "up", "down", "sfpAbsent", "trunking", "channelDown", "outofServc"]

