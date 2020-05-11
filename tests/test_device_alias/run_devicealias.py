from mdssdk.switch import Switch
import unittest

import logging

logging.basicConfig(filename='test_devicealias.log', filemode='w', level=logging.DEBUG,
					format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

import json

with open('../switch_details.json', 'r') as j:
	data = json.load(j)

sw = Switch(ip_address=data['ip_address'], username=data['username'], password=data['password'],
			connection_type=data['connection_type'], port=data['port'], timeout=data['timeout'],
			verify_ssl=False)

from tests.test_device_alias.test_devicealiasattrdatabase import *

TestDeviceAliasAttrDatabase.switch = sw
TestDeviceAliasAttrDatabase.new = {'da1': '60:66:61:01:0e:00:01:fe'}

from tests.test_device_alias.test_devicealiasattrdistribute import *

TestDeviceAliasAttrDistribute.switch = sw

from tests.test_device_alias.test_devicealiasattrlocked import *

TestDeviceAliasAttrLocked.switch = sw

from tests.test_device_alias.test_devicealiasattrmode import *

TestDeviceAliasAttrMode.switch = sw

from tests.test_device_alias.test_devicealiascleardatabase import *

TestDeviceAliasClearDatabase.switch = sw

from tests.test_device_alias.test_devicealiasclearlock import *

TestDeviceAliasClearLock.switch = sw

from tests.test_device_alias.test_devicealiascreate import *

TestDeviceAliasCreate.switch = sw
TestDeviceAliasCreate.new = {'da11': '50:66:61:01:0e:00:01:ff', 'da12': '51:66:61:01:0e:00:01:ff'}
TestDeviceAliasCreate.new_invalidname = {'da1&': '52:66:61:01:0e:00:01:ff'}  # da name a-zA-Z1-9 - _ $ ^    64chars max
TestDeviceAliasCreate.new_invalidfirstchar = {'1da': '53:66:61:01:0e:00:01:ff'}
TestDeviceAliasCreate.new_beyondmax = {
	'da123456789123456789123456789123456789123456789123456789123456789': '54:66:61:01:0e:00:01:ff'}
TestDeviceAliasCreate.new_max = {
	'd123456789123456789123456789123456789123456789123456789123456789': '55:66:61:01:0e:00:01:ff'}
TestDeviceAliasCreate.new_existingname = {'da13': '56:66:61:01:0e:00:01:ff', 'da14': '56:66:61:01:0e:00:01:fe'}
TestDeviceAliasCreate.existingname = {'da13': '56:66:61:01:0e:00:01:fd'}
TestDeviceAliasCreate.new_existingpwwn = {'da15': '57:66:61:01:0e:00:01:ff', 'da16': '57:66:61:01:0e:00:01:fe'}
TestDeviceAliasCreate.existingpwwn = {'da17': '57:66:61:01:0e:00:01:ff'}

from tests.test_device_alias.test_devicealiasdelete import *

TestDeviceAliasDelete.switch = sw
TestDeviceAliasDelete.new = {'da1': '60:66:61:01:0e:00:01:ff', 'da2': '60:66:61:01:0e:00:01:fe'}
TestDeviceAliasDelete.new1 = {'da3': '60:66:61:01:0e:00:01:fc', 'da4': '60:66:61:01:0e:00:01:fd'}
TestDeviceAliasDelete.nonexisting = 'da5'

from tests.test_device_alias.test_devicealiasrename import *

TestDeviceAliasRename.switch = sw
TestDeviceAliasRename.new_1 = {'da6': '60:66:61:01:0e:00:01:fa'}
TestDeviceAliasRename.rename_1 = {'oldname': 'da6', 'newname': 'testda6'}
TestDeviceAliasRename.new_2 = {'da7': '60:66:61:01:0e:00:01:ef', 'da8': '60:66:61:01:0e:00:01:df'}
TestDeviceAliasRename.rename_2 = {'oldname': 'da7', 'newname': 'da8'}  # existing_new_name
TestDeviceAliasRename.new_3 = {'da9': '60:66:61:01:0e:00:01:cf'}
TestDeviceAliasRename.rename_3 = {'oldname': 'testda', 'newname': 'da10'}  # nonexisting_old_name

d = DeviceAlias(sw)
print("Getting a copy of current device-alias database")
database = d.database
print("Clearing device-alias database before tests")
d.clear_database()
print("Running tests...")
suite = unittest.TestLoader().discover('tests.test_device_alias', 'test_devicealias*.py')
unittest.TextTestRunner(verbosity=2, failfast=True).run(suite)

print("Clearing device-alias database after tests")
d.clear_database()
print("Creating original database after tests")
d.create(database)
