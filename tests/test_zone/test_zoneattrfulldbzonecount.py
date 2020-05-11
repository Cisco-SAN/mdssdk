import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan


class TestZoneAttrFulldbZoneCount(unittest.TestCase):

    def test_fulldb_zone_count_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        print("Full DB Zone Count : " + str(z.fulldb_zone_count))
        v.delete()

    def test_fulldb_zone_count_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        print("Full DB Zone Count(nonexisting) : " + str(z.fulldb_zone_count))
        v.delete()

    def test_fulldb_zone_count_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        with self.assertRaises(AttributeError) as e:
            z.fulldb_zone_count = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
