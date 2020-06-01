import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone


class TestZoneAttrMembers(unittest.TestCase):

    def test_members_read(self):
        i = self.vsan_id[0]
        v = Vsan(self.switch, i)
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        members = self.members_dict
        self.switch.config('fcalias name somefcalias vsan ' + str(i))
        z.add_members(members)
        self.assertEqual(len(members), len(z.members))
        log.debug("Zone members added : " + str(z.members))
        z.delete()
        v.delete()

    def test_members_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIsNone(z.members)
        v.delete()

    def test_members_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        z.create()
        with self.assertRaises(AttributeError) as e:
            z.members = []
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
