import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from tests.test_zone.zone_vars import *

log = logging.getLogger(__name__)

class TestZoneAttrLocked(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.vsandb = sw.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()
        self.z = Zone(self.switch, self.id, "test_zone")

    def test_locked_read(self):
        self.z.create()
        self.assertIn(self.z.locked, [True, False])

    def test_locked_read_nonexisting(self):
        self.assertFalse(self.z.locked)

    def test_locked_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.locked = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()