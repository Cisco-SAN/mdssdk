import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneSetAttrMembers(unittest.TestCase):

    def test_members_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        zoneset = ZoneSet(self.switch, v, self.zoneset_name[0])
        zoneset.create()
        zone1 = Zone(self.switch, v, self.zone_name[0])
        zone2 = Zone(self.switch, v, self.zone_name[1])
        zone1.create()
        zone2.create()
        members = [zone1, zone2]
        zoneset.add_members(members)
        self.assertEqual([zone.name for zone in members], list(zoneset.members.keys()))
        zone1.delete()
        zone2.delete()
        v.delete()

    def test_members_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[1])
        self.assertIsNone(z.members)
        v.delete()

    def test_members_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[2])
        with self.assertRaises(AttributeError) as e:
            z.members = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
