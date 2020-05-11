import unittest

from mdssdk.zoneset import ZoneSet, ZoneNotPresent
from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneSetAddMembers(unittest.TestCase):

    def test_add_members_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        zonename = self.zone_name[0]
        zone = Zone(self.switch, v, zonename)
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[0])
        with self.assertRaises(ZoneNotPresent) as e:
            zoneset.add_members([zone])
        self.assertEqual("ZoneNotPresent: The given zoneset member '" + str(
            zonename) + "' is not present in the switch. Please create the zone first.", str(e.exception))
        v.delete()

    def test_add_members(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        zone1 = Zone(self.switch, v, self.zone_name[1])
        zone2 = Zone(self.switch, v, self.zone_name[2])
        zone1.create()
        zone2.create()
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[1])
        members = [zone1, zone2]
        zoneset.add_members(members)
        self.assertEqual([zone.name for zone in members], list(zoneset.members.keys()))
        zone1.delete()
        zone2.delete()
        zoneset.delete()
        v.delete()

    def test_add_members_samezone(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        zone1 = Zone(self.switch, v, self.zone_name[3])
        zone2 = Zone(self.switch, v, self.zone_name[4])
        zone1.create()
        zone2.create()

        zoneset1 = ZoneSet(self.switch, v, self.zoneset_name[2])
        zoneset2 = ZoneSet(self.switch, v, self.zoneset_name[3])
        members = [zone1, zone2]
        zoneset1.add_members(members)
        zoneset2.add_members(members)

        self.assertEqual([zone.name for zone in members], list(zoneset1.members.keys()))
        self.assertEqual([zone.name for zone in members], list(zoneset2.members.keys()))

    def test_add_members_typeerror(self):
        v = Vsan(self.switch, self.vsan_id[3])
        v.create()
        zone = Zone(self.switch, v, self.zone_name[5])
        zone.create()
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[4])
        with self.assertRaises(AttributeError) as e:
            zoneset.add_members(zone.name)
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))
        v.delete()
