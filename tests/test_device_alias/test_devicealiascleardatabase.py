import unittest

from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasClearDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.olddb = self.d.database
        if self.olddb is None:
            self.name = get_random_string()
            self.pwwn = get_random_pwwn()
            self.d.create({self.name: self.pwwn})
            newdb = self.d.database
            self.assertIn(self.name, newdb.keys())
            self.assertEqual(self.pwwn, newdb[self.name])

    # def test_clear_database(self):
    #     self.d.clear_database()
    #     self.assertIsNone(self.d.database)

    def tearDown(self) -> None:
        if self.olddb is not None:
            currdb = self.d.database
            if currdb == self.olddb:
                pass
            else:
                self.d.create(self.olddb)
