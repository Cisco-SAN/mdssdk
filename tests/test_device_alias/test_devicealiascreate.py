import unittest

from mdssdk.devicealias import DeviceAlias
from mdssdk.connection_manager.errors import CLIError


class TestDeviceAliasCreate(unittest.TestCase):

    def test_create(self):
        d = DeviceAlias(self.switch)
        d.create(self.new)
        self.assertEqual(self.new, d.database)
        keys = list(self.new.keys())
        for k in keys:
            d.delete(k)

    def test_create_name_invalid(self):
        d = DeviceAlias(self.switch)
        name = list(self.new_invalidname.keys())[0]
        pwwn = list(self.new_invalidname.values())[0]
        with self.assertRaises(CLIError) as e:
            d.create(self.new_invalidname)
        self.assertEqual("The command \" device-alias database ;  device-alias name " + str(name) + " pwwn " + str(
            pwwn) + " ; \" gave the error \" Illegal character present in the name \".", str(e.exception))
        d.clear_lock()

    def test_create_name_invalidfirstchar(self):
        d = DeviceAlias(self.switch)
        name = list(self.new_invalidfirstchar.keys())[0]
        pwwn = list(self.new_invalidfirstchar.values())[0]
        with self.assertRaises(CLIError) as e:
            d.create(self.new_invalidfirstchar)
        self.assertEqual("The command \" device-alias database ;  device-alias name " + str(name) + " pwwn " + str(
            pwwn) + " ; \" gave the error \" Illegal first character. Name must start with a letter \".",
                         str(e.exception))
        d.clear_lock()

    def test_create_name_beyondmax(self):
        d = DeviceAlias(self.switch)
        name = list(self.new_beyondmax.keys())[0]
        pwwn = list(self.new_beyondmax.values())[0]
        with self.assertRaises(CLIError) as e:
            d.create(self.new_beyondmax)
        self.maxDiff = 1000
        self.assertEqual("The command \" device-alias database ;  device-alias name " + str(name) + " pwwn " + str(
            pwwn) + " ; \" gave the error \" % String exceeded max length of (64) \".", str(e.exception))

    def test_create_name_max(self):
        d = DeviceAlias(self.switch)
        name = list(self.new_max.keys())[0]
        d.create(self.new_max)
        self.assertEqual(self.new_max, d.database)
        d.delete(name)

    def test_create_pwwn_existing(self):
        d = DeviceAlias(self.switch)
        d.create(self.new_existingpwwn)
        name = list(self.existingpwwn.keys())[0]
        pwwn = list(self.existingpwwn.values())[0]
        with self.assertLogs(level='INFO') as l:
            d.create(self.existingpwwn)
        self.assertEqual('INFO:mdssdk.devicealias:The command : device-alias database ;  device-alias name ' + str(
            name) + ' pwwn ' + str(pwwn) + ' ;  was not executed because Device Alias already present', l.output[0])
        keys = list(self.new_existingpwwn.keys())
        for k in keys:
            d.delete(k)

    def test_create_name_existing(self):
        d = DeviceAlias(self.switch)
        d.create(self.new_existingname)
        name = list(self.existingname.keys())[0]
        pwwn = list(self.existingname.values())[0]
        with self.assertLogs(level='INFO') as l:
            d.create(self.existingname)
        self.assertEqual('INFO:mdssdk.devicealias:The command : device-alias database ;  device-alias name ' + str(
            name) + ' pwwn ' + str(pwwn) + ' ;  was not executed because Device Alias already present', l.output[0])
        keys = list(self.new_existingname.keys())
        for k in keys:
            d.delete(k)
