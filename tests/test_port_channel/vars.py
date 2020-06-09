import json
import logging

from mdssdk.switch import Switch

log = logging.getLogger(__name__)

with open('switch_details.json', 'r') as j:
    data = json.load(j)

log.info("Creating switch object")

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

trunk_values = ['on', 'off', 'auto']

channel_mode_values = ["active", "on"]

mode_values = ['E', 'F', 'Fx', 'NP', 'SD', 'auto']

speed_values_read = ['1', '2', '4', '8', '16', '32', '--']
speed_values_write = [1000, 2000, 4000, 8000, 16000, 'auto']