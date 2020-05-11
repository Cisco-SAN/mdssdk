import unittest

from mdssdk.vsan import Vsan, VsanNotPresent, InvalidInterface
from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel


class TestVsanAddInterfaces(unittest.TestCase):

    def test_addinterfaces_type_error(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[0])
        v.create()
        fc = Fc(switch=self.switch, name=self.fc_name[0])
        with self.assertRaises(TypeError) as e:
            v.add_interfaces(fc)
        self.assertEqual("'Fc' object is not iterable", str(e.exception))
        pc = PortChannel(self.switch, self.pc_id[0])
        with self.assertRaises(TypeError) as e:
            v.add_interfaces(pc)
        self.assertEqual("'PortChannel' object is not iterable", str(e.exception))
        v.delete()

    def test_addinterfaces(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[1])
        v.create()
        fc = Fc(switch=self.switch, name=self.fc_name[1])
        v.add_interfaces([fc])
        self.assertEqual(fc.name, v.interfaces[0].name)
        v.delete()
        v = Vsan(switch=self.switch, id=self.vsan_id[2])
        v.create()
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        v.add_interfaces([pc])
        self.assertEqual(pc.name, v.interfaces[0].name)
        pc.delete()
        v.delete()

    def test_addinterfaces_splitlist(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[3])
        v.create()
        fc1 = Fc(switch=self.switch, name=self.fc_name[2])
        fc2 = Fc(switch=self.switch, name=self.fc_name[3])
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        v.add_interfaces([fc1])
        v.add_interfaces([fc2])
        v.add_interfaces([pc])
        self.assertEqual(fc1.name, v.interfaces[0].name)
        self.assertEqual(fc2.name, v.interfaces[1].name)
        self.assertEqual(pc.name, v.interfaces[2].name)
        pc.delete()
        v.delete()

    def test_addinterfaces_list(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[4])
        v.create()
        fc1 = Fc(switch=self.switch, name=self.fc_name[4])
        fc2 = Fc(switch=self.switch, name=self.fc_name[5])
        pc4 = PortChannel(self.switch, self.pc_id[3])
        pc5 = PortChannel(self.switch, self.pc_id[4])
        pc4.create()
        pc5.create()
        l = [fc1, fc2, pc4, pc5]
        v.add_interfaces(l)
        self.assertEqual(fc1.name, v.interfaces[0].name)
        self.assertEqual(fc2.name, v.interfaces[1].name)
        self.assertEqual(pc4.name, v.interfaces[2].name)
        self.assertEqual(pc5.name, v.interfaces[3].name)
        pc4.delete()
        pc5.delete()
        v.delete()

    def test_addinterfaces_fc_invalid(self):
        i = self.vsan_id[5]
        v = Vsan(switch=self.switch, id=i)
        v.create()
        for name in self.invalid_fc:
            with self.assertRaises(CLIError) as e:
                fc = Fc(switch=self.switch, name=name)
                v.add_interfaces([fc])
            self.assertEqual('The command " vsan database ; vsan ' + str(
                i) + ' interface ' + str(name) + ' " gave the error " Invalid interface format ".', str(e.exception))
        v.delete()

    def test_addinterfaces_invalid(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[6])
        v.create()
        with self.assertRaises(AttributeError) as e:
            v.add_interfaces("asdfg")
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))
        v.delete()

    def test_addinterfaces_fc_multiple(self):
        v = []
        idx = 0
        fcidx = 8
        for i in self.vsan_id[10:]:
            v.append(Vsan(switch=self.switch, id=i))
            v[idx].create()
            fc = Fc(switch=self.switch, name=self.fc_name[fcidx])
            v[idx].add_interfaces([fc])
            self.assertEqual(i, v[idx].id)
            self.assertEqual(self.fc_name[fcidx], v[idx].interfaces[0].name)
            fcidx += 1
            idx += 1
        for vsan in v:
            vsan.delete()

    def test_addinterfaces_nonexistingvsan(self):
        i = self.vsan_id[7]
        v = Vsan(switch=self.switch, id=i)
        if v.id is not None:
            v.delete()
        with self.assertRaises(VsanNotPresent) as e:
            v.add_interfaces([Fc(switch=self.switch, name=self.fc_name[6])])
        self.assertEqual("VsanNotPresent: Vsan " + str(i) + " is not present on the switch.", str(e.exception))

    def test_addinterfaces_repeated(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[8])
        v.create()
        fc1 = Fc(switch=self.switch, name=self.fc_name[7])
        pc = PortChannel(self.switch, self.pc_id[5])
        pc.create()
        v.add_interfaces([fc1, fc1, fc1, fc1])
        self.assertEqual(fc1.name, v.interfaces[0].name)
        pc.delete()
        v.delete()

    def test_addinterfaces_portchannelnotpresent(self):
        i = self.vsan_id[9]
        v = Vsan(switch=self.switch, id=i)
        v.create()
        pc = PortChannel(self.switch, self.pc_id[6])
        with self.assertRaises(CLIError) as e:
            v.add_interfaces([pc])
        self.assertEqual(
            'The command " vsan database ; vsan ' + str(i) + ' interface port-channel' + str(
                self.pc_id[6]) + ' " gave the error " Invalid range ".',
            str(e.exception))
        v.delete()

    def tearDown(self):
        v = Vsan(switch=self.switch, id=1)
        for i in self.fc_name:
            v.add_interfaces([Fc(switch=self.switch, name=i)])
