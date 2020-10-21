import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrSmartZone(unittest.TestCase):
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
        self.old = self.z.smart_zone

    def test_smart_zone_read(self):
        self.assertIn(self.z.smart_zone, [True, False])

    def test_smart_zone_write(self):
        self.z.create()
        old = self.z.smart_zone
        self.z.smart_zone = True
        self.assertTrue(self.z.smart_zone)
        self.z.smart_zone = False
        self.assertFalse(self.z.smart_zone)
        self.z.smart_zone = old

    def test_smart_zone_write_invalid(self):
        with self.assertRaises(ValueError) as e:
            self.z.smart_zone = "asdf"
        self.assertEqual(
            "Smart zone value must be of typr bool, True/False", str(e.exception)
        )

    def tearDown(self) -> None:
        self.z.smart_zone = self.old
        self.v.delete()
