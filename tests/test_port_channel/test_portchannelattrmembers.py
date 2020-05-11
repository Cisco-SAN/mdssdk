import unittest

from mdssdk.portchannel import PortChannel
from mdssdk.fc import Fc

# one member, more than one member, unsupported interface

class TestPortChannelAttrMembers(unittest.TestCase):

    def test_members_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        self.assertIsNone(pc.members)

    def test_members_read(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        self.assertIsNone(pc.members)
        pc.delete()

    def test_members_read_one(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        fc1 = Fc(self.switch,self.fc_name[0])
        pc.add_members([fc1])
        self.assertIn(fc1.name,pc.members)
        pc.delete()

    def test_members_read_multiple(self):
        pc = PortChannel(self.switch, self.pc_id[3])
        pc.create()
        fc1 = Fc(self.switch, self.fc_name[1])
        fc2 = Fc(self.switch, self.fc_name[2])
        pc.add_members([fc1,fc2])
        self.assertIn(fc1.name,pc.members)
        self.assertIn(fc2.name, pc.members)
        pc.delete()

    # def test_members_read_unsupported(self):
    #     pc = PortChannel(self.switch, self.pc_id[5])
    #     pc.create()
    #     self.assertIsNotNone(pc.members)
    #     banner("Read members (skip unsupported) test passed")
    #     pc.delete()

    def test_members_write_error(self):
        pc = PortChannel(self.switch, self.pc_id[4])
        with self.assertRaises(AttributeError) as e:
            pc.members = []
        self.assertEqual("can't set attribute",str(e.exception))