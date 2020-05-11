import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan


class TestZoneSetAttrName(unittest.TestCase):

    def test_name_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        name = self.zoneset_name[0]
        z = ZoneSet(self.switch, v, name)
        z.create()
        self.assertEqual(name, z.name)
        z.delete()
        v.delete()

    def test_name_read_nonexisting(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[1])
        self.assertIsNone(z.name)
        v.delete()

    def test_name_write_error(self):
        v = Vsan(self.switch, self.vsan_id[2])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[2])
        with self.assertRaises(AttributeError) as e:
            z.name = "asdf"
        self.assertEqual('can\'t set attribute', str(e.exception))
        v.delete()
