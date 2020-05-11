import unittest
from mdssdk.vsan import Vsan
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel


class TestVsanAttrInterfaces(unittest.TestCase):

    def test_interfaces_read(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[0])
        v.create()
        fc = [Fc(switch=self.switch, name=self.fc_name[0]), Fc(switch=self.switch, name=self.fc_name[1])]
        v.add_interfaces(fc)
        self.assertEqual(self.fc_name[0], v.interfaces[0].name)
        self.assertEqual(self.fc_name[1], v.interfaces[1].name)
        v.delete()

    def test_interfaces_read_nonexistingvsan(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[1])
        if v.id is not None:
            v.delete()
        self.assertIsNone(v.interfaces)

    def test_interfaces_write_error(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[2])
        v.create()
        with self.assertRaises(AttributeError) as e:
            v.interfaces = [Fc(switch=self.switch, name=self.fc_name[0]), Fc(switch=self.switch, name=self.fc_name[1])]
        self.assertEqual("can't set attribute", str(e.exception))
        v.delete()

    def tearDown(self):
        v = Vsan(switch=self.switch, id=1)
        for i in self.fc_name:
            v.add_interfaces([Fc(switch=self.switch, name=i)])
