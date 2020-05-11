import unittest

from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanAttrState(unittest.TestCase):

    def test_state_read(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[0])
        v.create()
        v.suspend = True
        self.assertEqual("suspended", v.state)
        v.suspend = False
        self.assertEqual("active", v.state)
        v.delete()

    def test_state_read_nonexistingvsan(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[1])
        if v.id is not None:
            v.delete()
        self.assertIsNone(v.state)

    def test_state_write_error(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[2])
        v.create()
        with self.assertRaises(AttributeError) as e:
            v.state = "active"
        self.assertEqual("can't set attribute", str(e.exception))
        v.delete()
