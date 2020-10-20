import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrLocked(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()
        self.z = Zone(self.switch, "test_zone", self.id)

    def test_locked_read(self):
        self.z.create()
        self.assertIn(self.z.locked, [True, False])

    def test_locked_read_nonexisting(self):
        self.assertFalse(self.z.locked)

    def test_locked_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.locked = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
