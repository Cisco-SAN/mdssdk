import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasDelete(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.olddb = self.d.database
        if self.olddb is None:
            self.name = get_random_string()
            self.pwwn = get_random_pwwn()
        else:
            while True:
                self.name = get_random_string()
                self.pwwn = get_random_pwwn()
                if (
                        self.name not in self.olddb.keys()
                        and self.pwwn not in self.olddb.values()
                ):
                    break
        log.debug({self.name: self.pwwn})

    def test_delete(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])
        self.d.delete(self.name)
        newdb = self.d.database
        if newdb is not None:
            self.assertNotIn(self.name, newdb.keys())
            self.assertNotIn(self.pwwn, newdb.values())

    def test_delete_nonexisting(self):
        db = self.d.database
        while True:
            somename = get_random_string()
            if db is None or somename not in db.keys():
                break
        with self.assertRaises(CLIError) as e:
            self.d.delete(somename)
        self.assertIn("Device Alias not present", str(e.exception))

    def tearDown(self) -> None:
        try:
            self.d.delete(self.name)
        except CLIError as c:
            if "Device Alias not present" not in c.message:
                self.fail("Tear down failed: " + c.message)
        enddb = self.d.database
        if enddb is not None:
            self.assertEqual(enddb, self.olddb)
