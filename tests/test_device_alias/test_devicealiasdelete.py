import unittest

from mdssdk.devicealias import DeviceAlias
from mdssdk.connection_manager.errors import CLIError


class TestDeviceAliasDelete(unittest.TestCase):

    def test_delete(self):
        d = DeviceAlias(self.switch)
        d.create(self.new)
        keys = list(self.new.keys())
        d.delete(keys[0])
        self.assertIsNone(d.database.get(keys[0]))
        keys.remove(keys[0])
        for k in keys:
            d.delete(k)

    def test_delete_nonexisting(self):
        d = DeviceAlias(self.switch)
        d.create(self.new1)
        keys = list(self.new1.keys())
        d.delete(keys[0])
        with self.assertRaises(CLIError) as e:
            d.delete(keys[0])
        self.assertEqual('The command " device-alias database ; no device-alias name ' + str(keys[
                                                                                                 0]) + ' " gave the error " Device Alias not present\nPlease use \'show device-alias session rejected\' to display the rejected set of commands and for the device-alias best-practices recommendation. ".',
                         str(e.exception))
        keys.remove(keys[0])
        for k in keys:
            d.delete(k)

    def test_delete_emptydb(self):
        d = DeviceAlias(self.switch)
        d.clear_database()
        with self.assertRaises(CLIError) as e:
            d.delete(self.nonexisting)
        self.assertEqual('The command " device-alias database ; no device-alias name ' + str(
            self.nonexisting) + ' " gave the error " Device Alias not present\nPlease use \'show device-alias session rejected\' to display the rejected set of commands and for the device-alias best-practices recommendation. ".',
                         str(e.exception))
