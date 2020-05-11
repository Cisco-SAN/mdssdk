import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneAttrSmartZone(unittest.TestCase):

    def test_smart_zone_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        self.assertIn(z.smart_zone, ['enabled', 'disabled'])
        v.delete()

    def test_smart_zone_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIn(z.smart_zone, ['enabled', 'disabled'])
        v.delete()

    def test_smart_zone_write(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        z.create()
        old = z.smart_zone
        z.smart_zone = True
        self.assertEqual('enabled', z.smart_zone)
        z.smart_zone = False
        self.assertEqual('disabled', z.smart_zone)
        z.smart_zone = old
        v.delete()

    '''def test_smart_zone_write_invalid(self):
        v = Vsan(self.switch,self.vsan_id[3])
        v.create()
        z = Zone(self.switch, v, self.zone_name[3])
        z.create()
        with self.assertRaises(TypeError) as e:
            z.smart_zone = 'asdf'
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))
        v.delete()'''
