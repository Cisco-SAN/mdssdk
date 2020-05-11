from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_fc.log', filemode='w', level=logging.DEBUG,
					format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
	data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
			connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
			verify_ssl=False)

from tests.test_fc.test_fcattrtransceiver import *

TestFcAttrTransceiver.switch = sw

from tests.test_fc.test_fcattroutofservice import *

TestFcAttrOutOfService.switch = sw
TestFcAttrOutOfService.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrOutOfService.status_values = ["inactive", "notConnected", "errDisabled", "up", "down", "sfpAbsent"]

from tests.test_fc.test_fcattranalyticstype import *

TestFcAttrAnalyticsType.switch = sw
TestFcAttrAnalyticsType.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrAnalyticsType.values = ["scsi", "nvme", "all", None]

from tests.test_fc.test_fcattrcounters import *

TestFcAttrCounters.switch = sw

from tests.test_fc.test_fcattrdescription import *

TestFcAttrDescription.switch = sw
TestFcAttrDescription.fc_name = ["fc1/46", "fc1/47", "fc1/48"]

from tests.test_fc.test_fcattrmode import *

TestFcAttrMode.switch = sw
TestFcAttrMode.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrMode.modes_allowed = []  # ['E', 'F', 'Fx', 'NP', 'SD', 'auto']

from tests.test_fc.test_fcattrname import *

TestFcAttrName.switch = sw
TestFcAttrName.fc_name = ["fc1/46", "fc1/47"]

from tests.test_fc.test_fcattrspeed import *

TestFcAttrSpeed.switch = sw
TestFcAttrSpeed.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrSpeed.speeds_allowed = []  # [1000, 16000, 2000, 32000, 4000, 8000]

from tests.test_fc.test_fcattrstatus import *

TestFcAttrStatus.switch = sw
TestFcAttrStatus.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrStatus.status_values = ["inactive", "notConnected", "errDisabled", "up", "down"]

from tests.test_fc.test_fcattrtrunk import *

TestFcAttrTrunk.switch = sw
TestFcAttrTrunk.fc_name = ["fc1/46", "fc1/47", "fc1/48"]
TestFcAttrTrunk.trunk_values = ['on', 'off', 'auto']

suite = unittest.TestLoader().discover('tests.test_fc', 'test_fc*.py')
unittest.TextTestRunner(verbosity=2).run(suite)
