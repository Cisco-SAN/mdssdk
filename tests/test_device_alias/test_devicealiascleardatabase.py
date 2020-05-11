import unittest

from mdssdk.devicealias import DeviceAlias


class TestDeviceAliasClearDatabase(unittest.TestCase):

    def test_clear_database(self):
        d = DeviceAlias(self.switch)
        d.clear_database()
        self.assertIsNone(d.database)
