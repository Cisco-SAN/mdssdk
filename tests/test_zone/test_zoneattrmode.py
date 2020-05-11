import unittest

from mdssdk.zone import Zone, InvalidZoneMode
from mdssdk.vsan import Vsan
from mdssdk.constants import BASIC, ENHANCED


class TestZoneAttrMode(unittest.TestCase):

    def test_mode_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        self.assertIn(z.mode, [BASIC, ENHANCED])
        v.delete()

    def test_mode_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIn(z.mode, [BASIC, ENHANCED])
        v.delete()

    def test_mode_write(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        z.create()
        old = z.mode
        z.mode = BASIC
        self.assertEqual(BASIC, z.mode)
        z.mode = ENHANCED
        self.assertEqual(ENHANCED, z.mode)
        z.mode = old
        v.delete()

    def test_mode_write_invalid(self):
        v = Vsan(self.switch, self.vsan_id[3])
        v.create()
        z = Zone(self.switch, v, self.zone_name[3])
        z.create()
        mode = 'asdf'
        with self.assertRaises(InvalidZoneMode) as e:
            z.mode = mode
        self.assertEqual('InvalidZoneMode: Invalid zone mode ' + str(mode) + ' . Valid values are: basic,enhanced',
                         str(e.exception))
        v.delete()
