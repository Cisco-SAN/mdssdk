from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_zone.log', filemode='w', level=logging.DEBUG,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
    data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
            connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
            verify_ssl=False)

import sys

sys.stdout = open('test_zone_output.txt', 'wt')

vsan_id = [2, 3, 4, 5, 6, 7, 8, 9]
zone_name = ["zone" + str(i) for i in range(1, 9)]

from mdssdk.fc import Fc
from mdssdk.devicealias import DeviceAlias
from mdssdk.portchannel import PortChannel

fc = Fc(sw, "fc1/48")
pc = PortChannel(sw, 1)
d = DeviceAlias(sw)
da_name = 'hello'
da_pwwn = '40:66:61:01:0e:00:01:ff'
d.create({da_name: da_pwwn})

members_dict = [{'pwwn': '50:08:01:60:08:9f:4d:00'},
                {'pwwn': '50:08:01:60:08:9f:4d:01'},
                {'interface': fc.name},
                {'device-alias': da_name},
                {'ip-address': '1.1.1.1'},
                {'symbolic-nodename': 'symbnodename'},
                {'fwwn': '11:12:13:14:15:16:17:18'},
                {'fcid': '0x123456'},
                {'interface': pc.name},
                {'symbolic-nodename': 'testsymnode'},
                {'fcalias': 'somefcalias'}]

fc1 = Fc(sw, "fc1/47")
pc1 = PortChannel(sw, 2)
members_list = [fc1, pc1, "10:99:88:90:76:88:99:ef"]

from tests.test_zone.test_zoneaddmembers import *

TestZoneAddMembers.switch = sw
TestZoneAddMembers.vsan_id = vsan_id
TestZoneAddMembers.zone_name = zone_name
TestZoneAddMembers.members_dict = members_dict
TestZoneAddMembers.members_list = members_list

from tests.test_zone.test_zoneremovemembers import *

TestZoneRemoveMembers.switch = sw
TestZoneRemoveMembers.vsan_id = vsan_id
TestZoneRemoveMembers.zone_name = zone_name
TestZoneRemoveMembers.members_dict = members_dict
TestZoneRemoveMembers.members_list = members_list

from tests.test_zone.test_zonecreate import *

TestZoneCreate.switch = sw
TestZoneCreate.vsan_id = vsan_id
TestZoneCreate.zone_name = zone_name
TestZoneCreate.zone_name_invalid = "zone1*!"  # zone name a-zA-Z1-9 - _ $ ^    64chars max
TestZoneCreate.zone_name_invalidfirstchar = "1zone"
TestZoneCreate.zone_name_beyondmax = 'zo123456789123456789123456789123456789123456789123456789123456789'
TestZoneCreate.zone_name_max = 'z123456789123456789123456789123456789123456789123456789123456789'

from tests.test_zone.test_zonedelete import *

TestZoneDelete.switch = sw
TestZoneDelete.vsan_id = vsan_id
TestZoneDelete.zone_name = zone_name

from tests.test_zone.test_zoneattrdefaultzone import *

TestZoneAttrDefaultZone.switch = sw
TestZoneAttrDefaultZone.vsan_id = vsan_id
TestZoneAttrDefaultZone.zone_name = zone_name

from tests.test_zone.test_zoneattrlocked import *

TestZoneAttrLocked.switch = sw
TestZoneAttrLocked.vsan_id = vsan_id
TestZoneAttrLocked.zone_name = zone_name

from tests.test_zone.test_zoneattrmembers import *

TestZoneAttrMembers.switch = sw
TestZoneAttrMembers.vsan_id = vsan_id
TestZoneAttrMembers.zone_name = zone_name
TestZoneAttrMembers.members_dict = members_dict

from tests.test_zone.test_zoneattrmode import *

TestZoneAttrMode.switch = sw
TestZoneAttrMode.vsan_id = vsan_id
TestZoneAttrMode.zone_name = zone_name

from tests.test_zone.test_zoneattrname import *

TestZoneAttrName.switch = sw
TestZoneAttrName.vsan_id = vsan_id
TestZoneAttrName.zone_name = zone_name

from tests.test_zone.test_zoneattrsmartzone import *

TestZoneAttrSmartZone.switch = sw
TestZoneAttrSmartZone.vsan_id = vsan_id
TestZoneAttrSmartZone.zone_name = zone_name

from tests.test_zone.test_zoneattrvsan import *

TestZoneAttrVsan.switch = sw
TestZoneAttrVsan.vsan_id = vsan_id
TestZoneAttrVsan.zone_name = zone_name

from tests.test_zone.test_zoneattrfulldbsize import *

TestZoneAttrFulldbSize.switch = sw
TestZoneAttrFulldbSize.vsan_id = vsan_id
TestZoneAttrFulldbSize.zone_name = zone_name

from tests.test_zone.test_zoneattrfulldbzonecount import *

TestZoneAttrFulldbZoneCount.switch = sw
TestZoneAttrFulldbZoneCount.vsan_id = vsan_id
TestZoneAttrFulldbZoneCount.zone_name = zone_name

from tests.test_zone.test_zoneattrfulldbzonesetcount import *

TestZoneAttrFulldbZonesetCount.switch = sw
TestZoneAttrFulldbZonesetCount.vsan_id = vsan_id
TestZoneAttrFulldbZonesetCount.zone_name = zone_name

from tests.test_zone.test_zoneattractivedbsize import *

TestZoneAttrActivedbSize.switch = sw
TestZoneAttrActivedbSize.vsan_id = vsan_id
TestZoneAttrActivedbSize.zone_name = zone_name

from tests.test_zone.test_zoneattractivedbzonecount import *

TestZoneAttrActivedbZoneCount.switch = sw
TestZoneAttrActivedbZoneCount.vsan_id = vsan_id
TestZoneAttrActivedbZoneCount.zone_name = zone_name

from tests.test_zone.test_zoneattractivedbzonesetcount import *

TestZoneAttrActivedbZonesetCount.switch = sw
TestZoneAttrActivedbZonesetCount.vsan_id = vsan_id
TestZoneAttrActivedbZonesetCount.zone_name = zone_name

from tests.test_zone.test_zoneattractivedbzonesetname import *

TestZoneAttrActivedbZonesetName.switch = sw
TestZoneAttrActivedbZonesetName.vsan_id = vsan_id
TestZoneAttrActivedbZonesetName.zone_name = zone_name

from tests.test_zone.test_zoneattrmaxdbsize import *

TestZoneAttrMaxdbSize.switch = sw
TestZoneAttrMaxdbSize.vsan_id = vsan_id
TestZoneAttrMaxdbSize.zone_name = zone_name

from tests.test_zone.test_zoneattreffectivedbsize import *

TestZoneAttrEffectivedbSize.switch = sw
TestZoneAttrEffectivedbSize.vsan_id = vsan_id
TestZoneAttrEffectivedbSize.zone_name = zone_name

from tests.test_zone.test_zoneattreffectivedbsizepercentage import *

TestZoneAttrEffectivedbSizePercentage.switch = sw
TestZoneAttrEffectivedbSizePercentage.vsan_id = vsan_id
TestZoneAttrEffectivedbSizePercentage.zone_name = zone_name

from tests.test_zone.test_zoneattrstatus import *

TestZoneAttrStatus.switch = sw
TestZoneAttrStatus.vsan_id = vsan_id
TestZoneAttrStatus.zone_name = zone_name

suite = unittest.TestLoader().discover('tests.test_zone', 'test_zone*.py')
unittest.TextTestRunner(verbosity=2).run(suite)

d.delete(da_name)
