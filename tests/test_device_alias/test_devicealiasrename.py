import unittest

from mdssdk.devicealias import DeviceAlias
from mdssdk.connection_manager.errors import CLIError


class TestDeviceAliasRename(unittest.TestCase):

    def test_rename(self):
        d = DeviceAlias(self.switch)
        d.create(self.new_1)
        oldname = self.rename_1['oldname']
        newname = self.rename_1['newname']
        d.rename(oldname=oldname, newname=newname)
        self.assertEqual(self.new_1[oldname], d.database[newname])
        for k in self.new_1.keys():
            if (k == oldname):
                d.delete(newname)
                continue
            d.delete(k)

    def test_rename_existingnew(self):
        d = DeviceAlias(self.switch)
        d.create(self.new_2)
        oldname = self.rename_2['oldname']
        newname = self.rename_2['newname']
        with self.assertRaises(CLIError) as e:
            d.rename(oldname=oldname, newname=newname)
        self.assertEqual('The command " device-alias database ; device-alias rename ' + str(oldname) + ' ' + str(
            newname) + ' " gave the error " Target device-alias name already in use. Please specify a new name.\nPlease use \'show device-alias session rejected\' to display the rejected set of commands and for the device-alias best-practices recommendation. ".',
                         str(e.exception))
        for k in self.new_2.keys():
            d.delete(k)

    def test_rename_nonexistingold(self):
        d = DeviceAlias(self.switch)
        d.create(self.new_3)
        oldname = self.rename_3['oldname']
        newname = self.rename_3['newname']
        with self.assertRaises(CLIError) as e:
            d.rename(oldname=oldname, newname=newname)
        self.assertEqual('The command " device-alias database ; device-alias rename ' + str(oldname) + ' ' + str(
            newname) + ' " gave the error " Device Alias not present\nPlease use \'show device-alias session rejected\' to display the rejected set of commands and for the device-alias best-practices recommendation. ".',
                         str(e.exception))
        for k in self.new_3.keys():
            d.delete(k)

    def test_rename_emptydb(self):
        d = DeviceAlias(self.switch)
        d.clear_database()
        with self.assertRaises(CLIError) as e:
            d.rename(oldname='da2', newname='da3')
        self.assertEqual(
            'The command " device-alias database ; device-alias rename da2 da3 " gave the error " Device Alias not present\nPlease use \'show device-alias session rejected\' to display the rejected set of commands and for the device-alias best-practices recommendation. ".',
            str(e.exception))
