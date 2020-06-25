import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasAttrLocked(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.old = self.d.distribute
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

    def test_locked_values(self):
        self.assertIn(self.d.locked, [True, False])

    def test_locked_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.d.locked = True
        self.assertEqual("can't set attribute", str(e.exception))

    def test_acquire_lock(self):
        # Verify that lock is not acquired first
        self.assertFalse(self.d.locked)
        # Verify that distribute is set
        if not self.old:
            self.d.distribute = True
            self.assertTrue(self.d.distribute)
        self.switch.config(
            "device-alias database ; device-alias name "
            + self.name
            + " pwwn "
            + self.pwwn
        )
        self.assertTrue(self.d.locked)
        self.d.clear_lock()
        self.assertFalse(self.d.locked)
        self.d.distribute = self.old
        self.assertFalse(self.d.locked)

    def tearDown(self) -> None:
        self.d.distribute = self.old
        self.assertEqual(self.d.distribute, self.old)
        try:
            self.d.delete(self.name)
            newdb = self.d.database
            if newdb is not None:
                self.assertNotIn(self.name, newdb.keys())
                self.assertNotIn(self.pwwn, newdb.values())
        except CLIError as c:
            if "Device Alias not present" not in c.message:
                raise CLIError(c.args)
        finally:
            self.assertFalse(self.d.locked)
