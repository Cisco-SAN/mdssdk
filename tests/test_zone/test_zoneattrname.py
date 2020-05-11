import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan


class TestZoneAttrName(unittest.TestCase):

    def test_name_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        zonename = self.zone_name[0]
        z = Zone(self.switch, v, zonename)
        z.create()
        self.assertEqual(zonename, z.name)
        v.delete()

    def test_name_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIsNone(z.name)
        v.delete()

    def test_name_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        with self.assertRaises(AttributeError) as e:
            z.name = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
