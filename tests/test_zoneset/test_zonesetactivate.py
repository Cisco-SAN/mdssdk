import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneSetActivate(unittest.TestCase):

    def test_activate(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[0])
        zoneset.create()
        zone = Zone(self.switch, v, self.zone_name[0])
        zone.create()
        zone.add_members(self.zone_members)
        zoneset.add_members([zone])

        zoneset.activate(True)
        self.assertTrue(zoneset.is_active())

        zoneset.activate(False)
        self.assertFalse(zoneset.is_active())

        zone.delete()
        zoneset.delete()
        v.delete()

    def test_activate_zonehasnomembers(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[1])
        zoneset.create()
        zone = Zone(self.switch, v, self.zone_name[1])
        zone.create()
        zoneset.add_members([zone])

        zoneset.activate(True)  # not activated since zone has no members
        self.assertFalse(zoneset.is_active())

        zone.delete()
        zoneset.delete()
        v.delete()

    def test_activate_multiple(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()

        zoneset = ZoneSet(self.switch, v, self.zoneset_name[2])
        zoneset.create()
        zone = Zone(self.switch, v, self.zone_name[2])
        zone.create()
        zone.add_members(self.zone_members)
        zoneset.add_members([zone])
        zoneset.activate(True)
        self.assertTrue(zoneset.is_active())

        zoneset1 = ZoneSet(self.switch, v, self.zoneset_name[3])
        zoneset1.create()
        zoneset1.add_members([zone])

        zoneset1.activate(True)
        self.assertTrue(zoneset1.is_active())
        self.assertFalse(zoneset.is_active())

        zone.delete()
        zoneset.delete()
        zoneset1.delete()
        v.delete()
