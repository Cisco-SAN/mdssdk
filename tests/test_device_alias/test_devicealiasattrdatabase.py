import unittest

from mdssdk.devicealias import DeviceAlias


class TestDeviceAliasAttrDatabase(unittest.TestCase):

    def test_database_read(self):
        d = DeviceAlias(self.switch)
        d.create(self.new)
        self.assertEquals(self.new, d.database)
        for da in self.new.keys():
            d.delete(da)

    def test_database_write_error(self):
        d = DeviceAlias(self.switch)
        with self.assertRaises(AttributeError) as e:
            d.database = self.new
        self.assertEqual('can\'t set attribute', str(e.exception))
