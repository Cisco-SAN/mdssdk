import unittest

from mdssdk.devicealias import DeviceAlias, InvalidMode
from mdssdk.constants import BASIC, ENHANCED


class TestDeviceAliasAttrMode(unittest.TestCase):

    def test_mode_read(self):
        d = DeviceAlias(self.switch)
        self.assertIn(d.mode.lower(), [BASIC, ENHANCED])

    def test_mode_write(self):
        d = DeviceAlias(self.switch)
        old = d.mode
        d.mode = ENHANCED
        self.assertEqual(ENHANCED, d.mode.lower())
        d.mode = BASIC
        self.assertEqual(BASIC, d.mode.lower())
        d.mode = old

    def test_mode_write_invalid(self):
        d = DeviceAlias(self.switch)
        mode = 'asdf'
        with self.assertRaises(InvalidMode) as e:
            d.mode = mode
        self.assertEqual(
            "InvalidMode: Invalid device alias mode: " + str(mode) + ". Valid values are " + ENHANCED + "," + BASIC,
            str(e.exception))
