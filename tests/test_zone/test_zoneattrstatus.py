import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.zoneset import ZoneSet

class TestZoneAttrStatus(unittest.TestCase):

    def test_status_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        zoneset = ZoneSet(self.switch, v, "test_zoneset")
        zoneset.create()   
        z.add_members([{'fcid': '0x123456'}])
        zoneset.add_members([z])
        zoneset.activate(True)
        if(zoneset.is_active()):
            self.assertIn("Activation", z.status)
        else:
            self.assertIsNotNone(z.status)
        v.delete()

    def test_status_read_nonexisting(self):
        v = Vsan(self.switch,self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        self.assertIsNotNone(z.status)
        v.delete()

    def test_status_write_error(self):
        v = Vsan(self.switch,self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        with self.assertRaises(AttributeError) as e:
            z.status = "asdf"
        self.assertEqual('can\'t set attribute',str(e.exception))
        v.delete()