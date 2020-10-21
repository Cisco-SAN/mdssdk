import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetActivate(unittest.TestCase):
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
        self.zone = Zone(self.switch, "test_zone", self.id)
        self.zone.create()
        self.zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        self.zoneset.create()
        self.zone_members = members_dict

    def test_activate(self):
        self.zone.add_members(self.zone_members)
        self.zoneset.add_members([self.zone])

        self.zoneset.activate(True)
        self.assertTrue(self.zoneset.is_active())

        self.zoneset.activate(False)
        self.assertFalse(self.zoneset.is_active())

    def test_activate_zonehasnomembers(self):
        self.zoneset.add_members([self.zone])

        self.zoneset.activate(True)  # not activated since zone has no members
        self.assertFalse(self.zoneset.is_active())

    def test_activate_multiple(self):
        self.zone.add_members(self.zone_members)
        self.zoneset.add_members([self.zone])
        self.zoneset.activate(True)
        self.assertTrue(self.zoneset.is_active())

        zoneset1 = ZoneSet(self.switch, "test_zoneset_2", self.id)
        zoneset1.create()
        zoneset1.add_members([self.zone])

        zoneset1.activate(True)
        self.assertTrue(zoneset1.is_active())
        self.assertFalse(self.zoneset.is_active())

    def tearDown(self) -> None:
        self.v.delete()
