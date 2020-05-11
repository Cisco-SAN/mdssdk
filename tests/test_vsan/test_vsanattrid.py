import unittest
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanAttrId(unittest.TestCase):

    def test_id_read(self):
        i = self.vsan_id
        v = Vsan(switch=self.switch, id=i)
        v.create()
        self.assertEqual(i, v.id)
        v.delete()

    def test_id_read_nonexistingvsan(self):
        v = Vsan(switch=self.switch, id=self.vsan_id)
        if v.id is not None:
            v.delete()
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            self.assertIsNone(v.id)
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            self.assertEqual(i, v.id)

    def test_id_write_error(self):
        v = Vsan(switch=self.switch, id=self.vsan_id)
        v.create()
        with self.assertRaises(AttributeError) as e:
            v.id = 4
        self.assertEqual("can't set attribute", str(e.exception))
        v.delete()
