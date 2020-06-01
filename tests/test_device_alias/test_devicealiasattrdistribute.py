import unittest

from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.da_vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasAttrDistribute(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.old = self.d.distribute

    def test_distribute_read(self):
        self.assertIn(self.d.distribute, [True, False])

    def test_distribute_write(self):
        if self.old:
            self.d.distribute = False
            self.assertFalse(self.d.distribute)
        else:
            self.d.distribute = True
            self.assertTrue(self.d.distribute)
        self.d.distribute = self.old
        self.assertEqual(self.d.distribute, self.old)

    def tearDown(self) -> None:
        self.d.distribute = self.old
        self.assertEqual(self.d.distribute, self.old)
