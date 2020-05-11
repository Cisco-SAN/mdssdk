import unittest

from mdssdk.devicealias import DeviceAlias


class TestDeviceAliasClearLock(unittest.TestCase):

    def test_clear_lock(self):
        d = DeviceAlias(self.switch)
        d.clear_lock()
        self.assertEqual(False, d.locked)
