import unittest

from mdssdk.devicealias import DeviceAlias


class TestDeviceAliasAttrDistribute(unittest.TestCase):

    def test_distribute_read(self):
        d = DeviceAlias(self.switch)
        self.assertIn(d.distribute, [True, False])

    def test_distribute_write(self):
        d = DeviceAlias(self.switch)
        old = d.distribute
        d.distribute = True
        self.assertTrue(d.distribute)
        d.distribute = False
        self.assertFalse(d.distribute)
        d.distribute = old
