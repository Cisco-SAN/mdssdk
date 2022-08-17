import random
import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrActiveZonesets(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = random.randint(2, 400)
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()

    def test_active_zonesets_read(self):
        if self.switch.npv:
            self.skipTest("Switch in NPV mode")
        zone = Zone(self.switch, "test_zone", self.id)
        zone.create()
        zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        zoneset.create()
        zone.add_members([{"fcid": "0x123456"}])
        zoneset.add_members([zone])
        zoneset.activate(True)
        active_zonesets = self.switch.active_zonesets
        self.assertIn(self.v.id, list(active_zonesets.keys()))

    def test_active_zonesets_write_error(self):
        if self.switch.npv:
            self.skipTest("Switch in NPV mode")
        with self.assertRaises(AttributeError) as e:
            self.switch.active_zonesets = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
