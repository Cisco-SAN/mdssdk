import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan


class TestZoneSetAttrVsan(unittest.TestCase):

    def test_vsan_read(self):
        i = self.vsan_id[0]
        v = Vsan(self.switch, i)
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[0])
        z.create()
        self.assertEqual(i, z.vsan.id)
        z.delete()
        v.delete()

    def test_vsan_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[1])
        self.assertIsNone(z.vsan)
        v.delete()

    def test_vsan_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[2])
        z.create()
        with self.assertRaises(AttributeError) as e:
            z.vsan = 5
        self.assertEqual('can\'t set attribute', str(e.exception))
        z.delete()
        v.delete()
