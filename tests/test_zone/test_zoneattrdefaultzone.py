import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from mdssdk.constants import PERMIT, DENY


class TestZoneAttrDefaultZone(unittest.TestCase):

    def test_default_zone_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        self.assertIn(z.default_zone, [PERMIT, DENY])
        v.delete()

    def test_default_zone_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIn(z.default_zone, [PERMIT, DENY])
        v.delete()

    def test_default_zone_write(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        z.create()
        old = z.default_zone
        z.default_zone = DENY
        self.assertEqual(DENY, z.default_zone)
        z.default_zone = PERMIT
        self.assertEqual(PERMIT, z.default_zone)
        z.default_zone = old
        v.delete()

    def test_default_zone_write_invalid(self):
        v = Vsan(self.switch, self.vsan_id[3])
        v.create()
        z = Zone(self.switch, v, self.zone_name[3])
        z.create()
        default_zone = 'asdf'
        with self.assertRaises(CLIError) as e:
            z.default_zone = default_zone
        self.assertEqual('The command " No cmd sent " gave the error " Invalid default-zone value ' + str(
            default_zone) + ' . Valid values are: permit,deny ".', str(e.exception))
        v.delete()
