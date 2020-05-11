import unittest

from mdssdk.portchannel import PortChannel,PortChannelNotPresent
from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelAddMembers(unittest.TestCase):

    def test_add_members_paramtype(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[0])
        with self.assertRaises(TypeError) as e:
            pc.add_members(fc1)
        self.assertEqual("'Fc' object is not iterable",str(e.exception))
        pc.delete()

    def test_add_members_one(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[1])
        pc.add_members([fc1])
        self.assertIn(fc1.name, pc.members)
        pc.delete()

    def test_add_members_multiple(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[2])
        fc2 = Fc(self.switch, self.fc_name[3])
        pc.add_members([fc1, fc2])
        self.assertIn(fc1.name, pc.members)
        self.assertIn(fc2.name, pc.members)
        pc.delete()

    def test_add_members_nonexisting(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        fc1 = Fc(self.switch, self.fc_name[4])
        with self.assertRaises(PortChannelNotPresent) as e:
            pc.add_members([fc1])
        self.assertEqual("PortChannelNotPresent: Port channel " + str(i) + " is not present on the switch, please create the PC first", str(e.exception))

    def test_add_members_invalidfc(self):
        i = self.pc_id[4]
        pc = PortChannel(self.switch, i)
        pc.create()
        invalidfc = self.invalid_fc
        fc1 = Fc(self.switch, invalidfc)
        with self.assertRaises(CLIError) as e:
            pc.add_members([fc1])
        self.assertEqual("The command \" interface "+str(invalidfc)+" ; channel-group "+str(i)+" force \" gave the error \" Invalid interface format \".", str(e.exception))
        pc.delete()

    def test_add_members_invalid(self):
        pc = PortChannel(self.switch, self.pc_id[5])
        pc.create()
        with self.assertRaises(AttributeError) as e:
            pc.add_members([self.fc_name[5]])
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))
        pc.delete()


