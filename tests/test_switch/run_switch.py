from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_switch.log', filemode='w', level=logging.DEBUG,
					format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
	data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
			connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
			verify_ssl=False)

import sys

sys.stdout = open('test_switch_output.txt', 'wt')

from tests.test_switch.test_switchshow import *

TestSwitchShow.switch = sw
TestSwitchShow.commands = "show vsan usage"

from tests.test_switch.test_switchshowlist import *

TestSwitchShowList.switch = sw
TestSwitchShowList.commands = ["show vsan usage", "show module"]

from tests.test_switch.test_switchconfig import *

TestSwitchConfig.switch = sw
TestSwitchConfig.commands = "vsan database ; vsan 2 ; terminal dont-ask ; no vsan 2 ; no terminal dont-ask"
TestSwitchConfig.commands_clierror = "terminal dont-ask ; vsan database ; no vsan 2 "

from tests.test_switch.test_switchconfiglist import *

TestSwitchConfigList.switch = sw
TestSwitchConfigList.commands = ["vsan database ; vsan 2 ; terminal dont-ask ; no vsan 2 ", "no terminal dont-ask"]
TestSwitchConfigList.commands_clierror = ["vsan database ; terminal dont-ask ; no vsan 2 "]

from tests.test_switch.test_switchattripaddr import *

TestSwitchAttrIpAddr.switch = sw
TestSwitchAttrIpAddr.ip_address = data['ip_address']

from tests.test_switch.test_switchattrformfactor import *

TestSwitchAttrFormFactor.switch = sw

from tests.test_switch.test_switchattrtype import *

TestSwitchAttrType.switch = sw

from tests.test_switch.test_switchattrname import *

TestSwitchAttrName.switch = sw
TestSwitchAttrName.name_max32 = "switch12345678912345678912345678"  # len 32
TestSwitchAttrName.name_beyondmax = "switch123456789123456789123456789"  # len 33
TestSwitchAttrName.invalid_name = "1"  # starts with digit

from tests.test_switch.test_switchattrversion import *

TestSwitchAttrVersion.switch = sw

from tests.test_switch.test_switchattrmodel import *

TestSwitchAttrModel.switch = sw

from tests.test_switch.test_switchattrmodules import *

TestSwitchAttrModules.switch = sw

from tests.test_switch.test_switchattrnpv import *

TestSwitchAttrNpv.switch = sw

from tests.test_switch.test_switchattrimagestring import *

TestSwitchAttrImageString.switch = sw

from tests.test_switch.test_switchattrkickstartimage import *

TestSwitchAttrKickstartImage.switch = sw

from tests.test_switch.test_switchattrsystemimage import *

TestSwitchAttrSystemImage.switch = sw

from tests.test_switch.test_switchattrvsans import *

TestSwitchAttrVsans.switch = sw

from tests.test_switch.test_switchattrinterfaces import *

TestSwitchAttrInterfaces.switch = sw

from tests.test_switch.test_switchattranalytics import *

TestSwitchAttrAnalytics.switch = sw

suite = unittest.TestLoader().discover('tests.test_switch', 'test_switch*.py')
unittest.TextTestRunner(verbosity=2).run(suite)
