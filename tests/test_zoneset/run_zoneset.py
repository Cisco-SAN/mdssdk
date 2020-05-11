from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_zoneset.log', filemode='w', level=logging.DEBUG,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

import sys

sys.stdout = open('test_zoneset_output.txt', 'wt')

members_dict = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
                {'pwwn': '50:08:01:60:08:9f:4d:01'},
                {'ip-address': '1.1.1.1'},
                {'symbolic-nodename': 'symbnodename'},
                {'fwwn': '11:12:13:14:15:16:17:18'},
                {'fcid': '0x123456'},
                {'symbolic-nodename': 'testsymnode'}]

vsan_id = range(3,12)
zone_name = ["zone" + str(i) for i in range(2, 9)]
zoneset_name = ["zoneset" + str(i) for i in range(2, 9)]

from tests.test_zoneset.test_zonesetcreate import *

TestZoneSetCreate.switch = sw
TestZoneSetCreate.vsan_id = vsan_id
TestZoneSetCreate.zoneset_name = zoneset_name
TestZoneSetCreate.zoneset_name_invalid = "zoneset1*!"
TestZoneSetCreate.zoneset_name_invalidfirstchar = "1zoneset"
TestZoneSetCreate.zoneset_name_beyondmax = 'zo123456789123456789123456789123456789123456789123456789123456789'
TestZoneSetCreate.zoneset_name_max = 'z123456789123456789123456789123456789123456789123456789123456789'
TestZoneSetCreate.zoneset_max_range = range(0, 1000)  #

from tests.test_zoneset.test_zonesetdelete import *

TestZoneSetDelete.switch = sw
TestZoneSetDelete.vsan_id = vsan_id
TestZoneSetDelete.zoneset_name = zoneset_name

from tests.test_zoneset.test_zonesetaddmembers import *

TestZoneSetAddMembers.switch = sw
TestZoneSetAddMembers.vsan_id = vsan_id
TestZoneSetAddMembers.zone_name = zone_name
TestZoneSetAddMembers.zoneset_name = zoneset_name

from tests.test_zoneset.test_zonesetremovemembers import *

TestZoneSetRemoveMembers.switch = sw
TestZoneSetRemoveMembers.vsan_id = vsan_id
TestZoneSetRemoveMembers.zone_name = zone_name
TestZoneSetRemoveMembers.zoneset_name = zoneset_name

from tests.test_zoneset.test_zonesetactivate import *

TestZoneSetActivate.switch = sw
TestZoneSetActivate.vsan_id = vsan_id
TestZoneSetActivate.zone_name = zone_name
TestZoneSetActivate.zoneset_name = zoneset_name
TestZoneSetActivate.zone_members = members_dict

from tests.test_zoneset.test_zonesetisactive import *

TestZoneSetIsActive.switch = sw
TestZoneSetIsActive.vsan_id = vsan_id
TestZoneSetIsActive.zone_name = zone_name
TestZoneSetIsActive.zoneset_name = zoneset_name
TestZoneSetIsActive.zone_members = members_dict

from tests.test_zoneset.test_zonesetattrname import *

TestZoneSetAttrName.switch = sw
TestZoneSetAttrName.vsan_id = vsan_id
TestZoneSetAttrName.zoneset_name = zoneset_name

from tests.test_zoneset.test_zonesetattrmembers import *

TestZoneSetAttrMembers.switch = sw
TestZoneSetAttrMembers.vsan_id = vsan_id
TestZoneSetAttrMembers.zone_name = zone_name
TestZoneSetAttrMembers.zoneset_name = zoneset_name

from tests.test_zoneset.test_zonesetattrvsan import *

TestZoneSetAttrVsan.switch = sw
TestZoneSetAttrVsan.vsan_id = vsan_id
TestZoneSetAttrVsan.zoneset_name = zoneset_name

suite = unittest.TestLoader().discover('tests.test_zoneset', 'test_zoneset*.py')
unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
