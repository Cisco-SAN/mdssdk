import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan


class TestZoneAttrActivedbZonesetName(unittest.TestCase):

    def test_activedb_zoneset_name_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        print("Active DB Zoneset Name : " + str(z.activedb_zoneset_name))
        v.delete()

    def test_activedb_zoneset_name_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        print("Active DB Zoneset Name(nonexisting) : " + str(z.activedb_zoneset_name))
        v.delete()

    def test_activedb_zoneset_name_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        with self.assertRaises(AttributeError) as e:
            z.activedb_zoneset_name = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
