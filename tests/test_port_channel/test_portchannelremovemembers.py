import unittest

from mdssdk.portchannel import PortChannel,PortChannelNotPresent
from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelRemoveMembers(unittest.TestCase):

    def test_remove_members_paramtype(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[0])
        pc.add_members([fc1])
        with self.assertRaises(TypeError) as e:
            pc.remove_members(fc1)
        self.assertEqual("'Fc' object is not iterable",str(e.exception))
        pc.delete()

    def test_remove_members_one(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[1])
        fc2 = Fc(self.switch, self.fc_name[2])
        pc.add_members([fc1, fc2])
        pc.remove_members([fc1])
        self.assertNotIn(fc1.name, pc.members)
        pc.delete()

    def test_remove_members_multiple(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[3])
        fc2 = Fc(self.switch, self.fc_name[4])
        pc.add_members([fc1, fc2])
        pc.remove_members([fc1, fc2])
        self.assertIsNone(pc.members)
        pc.delete()

    def test_remove_members_nonexistingpc(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        fc1 = Fc(self.switch, self.fc_name[5])
        with self.assertRaises(PortChannelNotPresent) as e:
            pc.add_members([fc1])
        self.assertEqual("PortChannelNotPresent: Port channel " + str(i) + " is not present on the switch, please create the PC first", str(e.exception))

    def test_remove_members_nonexisting(self):
        i = self.pc_id[4]
        pc = PortChannel(self.switch, i)
        pc.create()
        fcname = self.fc_name[6]
        fc1 = Fc(self.switch, fcname )
        with self.assertRaises(CLIError) as e:
            pc.remove_members([fc1])
        self.assertEqual("The command \" interface "+str(fcname)+" ; no channel-group "+str(i)+" \" gave the error \" "+str(fcname)+": not part of port-channel \".", str(e.exception))
        pc.delete()


