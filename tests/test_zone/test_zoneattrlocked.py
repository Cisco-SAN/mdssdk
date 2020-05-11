import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan


class TestZoneAttrLocked(unittest.TestCase):

    def test_locked_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        self.assertIn(z.locked, [True, False])
        v.delete()

    def test_locked_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertFalse(z.locked)
        v.delete()

    def test_locked_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        z.create()
        with self.assertRaises(AttributeError) as e:
            z.locked = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
