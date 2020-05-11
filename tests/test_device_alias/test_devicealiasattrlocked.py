import unittest

from mdssdk.devicealias import DeviceAlias


class TestDeviceAliasAttrLocked(unittest.TestCase):

    def test_locked(self):
        d = DeviceAlias(self.switch)
        self.assertIn(d.locked, [True, False])

    def test_locked_write_error(self):
        d = DeviceAlias(self.switch)
        with self.assertRaises(AttributeError) as e:
            d.locked = True
        self.assertEqual('can\'t set attribute', str(e.exception))
