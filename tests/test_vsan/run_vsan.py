from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_vsan.log', filemode='w', level=logging.DEBUG,
					format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
	data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
			connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
			verify_ssl=False)

default_id = 1
boundary_id = [0, 4095]
reserved_id = [4079, 4094]
vsan_id = range(4050,4075)

from tests.test_vsan.test_vsancreate import *

TestVsanCreate.switch = sw
TestVsanCreate.create_id = vsan_id[10]
TestVsanCreate.boundary_id = boundary_id
TestVsanCreate.reserved_id = reserved_id
TestVsanCreate.max_vsan_fail = range(2, 256)
TestVsanCreate.max_vsan_success = range(2, 255)
TestVsanCreate.create_multiple_id = vsan_id[11]

from tests.test_vsan.test_vsandelete import *

TestVsanDelete.switch = sw
TestVsanDelete.delete_id = vsan_id[12]
TestVsanDelete.default_id = default_id
TestVsanDelete.nonexisting_id = vsan_id[13]
TestVsanDelete.boundary_id = boundary_id
TestVsanDelete.reserved_id = reserved_id

from tests.test_vsan.test_vsanaddinterfaces import *

TestVsanAddInterfaces.switch = sw
TestVsanAddInterfaces.vsan_id = vsan_id
TestVsanAddInterfaces.fc_name = ['fc1/' + str(i) for i in range(31, 49)]
TestVsanAddInterfaces.pc_id = [i for i in range(247, 257)]
TestVsanAddInterfaces.invalid_fc = ["fc2/1"]

from tests.test_vsan.test_vsanattrid import *

TestVsanAttrId.switch = sw
TestVsanAttrId.vsan_id = vsan_id[9]
TestVsanAttrId.boundary_id = boundary_id
TestVsanAttrId.reserved_id = reserved_id

from tests.test_vsan.test_vsanattrstate import *

TestVsanAttrState.switch = sw
TestVsanAttrState.vsan_id = vsan_id

from tests.test_vsan.test_vsanattrinterfaces import *

TestVsanAttrInterfaces.switch = sw
TestVsanAttrInterfaces.vsan_id = vsan_id
TestVsanAttrInterfaces.fc_name = ["fc1/47", "fc1/48"]

from tests.test_vsan.test_vsanattrname import *

TestVsanAttrName.switch = sw
TestVsanAttrName.vsan_id = vsan_id
TestVsanAttrName.boundary_id = boundary_id
TestVsanAttrName.reserved_id = reserved_id
TestVsanAttrName.max32_name = "12345678912345678912345678912345"
TestVsanAttrName.beyondmax_name = "123456789123456789123456789123456"

from tests.test_vsan.test_vsanattrsuspend import *

TestVsanAttrSuspend.switch = sw
TestVsanAttrSuspend.vsan_id = vsan_id
TestVsanAttrSuspend.boundary_id = boundary_id
TestVsanAttrSuspend.reserved_id = reserved_id

suite = unittest.TestLoader().discover('tests.test_vsan', 'test_vsan*.py')
unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)
