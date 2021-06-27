import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasAttrDistribute(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.old = self.d.distribute

    def test_distribute_read(self):
        self.assertIn(self.d.distribute, [True, False])

    def test_distribute_write(self):
        fab_not_stable_count = 0
        while True:
            try:
                if self.old:
                    self.d.distribute = False
                    self.assertFalse(self.d.distribute)
                else:
                    self.d.distribute = True
                    self.assertTrue(self.d.distribute)
                    self.d.distribute = self.old
                    self.assertEqual(self.d.distribute, self.old)
                break
            except CLIError as c:
                if "Fabric is not stable" in c.message:
                    fab_not_stable_count = fab_not_stable_count + 1
                    if fab_not_stable_count == 3:
                        self.skipTest(
                            "Skipping the test as changing the mode gave the error Fabric not stable"
                        )
                    continue
                raise CLIError(c.args)

    def tearDown(self) -> None:
        fab_not_stable_count = 0
        while True:
            try:
                self.d.distribute = self.old
                self.assertEqual(self.d.distribute, self.old)
                break
            except CLIError as c:
                if "Fabric is not stable" in c.message:
                    fab_not_stable_count = fab_not_stable_count + 1
                    if fab_not_stable_count == 3:
                        self.skipTest(
                            "Skipping the test as changing the mode gave the error Fabric not stable"
                        )
                    continue
                raise CLIError(c.command, c.message)
