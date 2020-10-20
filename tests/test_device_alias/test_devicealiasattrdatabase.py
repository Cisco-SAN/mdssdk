import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasAttrDatabase(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.d = DeviceAlias(self.switch)
        currdb = self.d.database
        if currdb is None:
            self.name = get_random_string()
            self.pwwn = get_random_pwwn()
        else:
            while True:
                self.name = get_random_string()
                self.pwwn = get_random_pwwn()
                if self.name not in currdb.keys() and self.pwwn not in currdb.values():
                    break
        log.debug({self.name: self.pwwn})

    def test_database_read(self):
        log.debug("Starting test test_database_read")
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])
        self.d.delete(self.name)
        newdb = self.d.database
        if newdb is not None:
            self.assertNotIn(self.name, newdb.keys())
            self.assertNotIn(self.pwwn, newdb.values())

    def test_database_write_error(self):
        log.debug("Starting test test_database_write_error")
        with self.assertRaises(AttributeError) as e:
            self.d.database = {self.name: self.pwwn}
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        try:
            self.d.delete(self.name)
            newdb = self.d.database
            if newdb is not None:
                self.assertNotIn(self.name, newdb.keys())
                self.assertNotIn(self.pwwn, newdb.values())
        except CLIError as c:
            if "Device Alias not present" not in c.message:
                # raise CLIError(c.args)
                raise CLIError(c.command, c.message)
