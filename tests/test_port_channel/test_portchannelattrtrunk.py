import unittest

from mdssdk.portchannel import PortChannel
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelAttrTrunk(unittest.TestCase):

    def test_trunk_read(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        self.assertIn(pc.trunk,self.trunk_values)
        pc.delete()

    def test_trunk_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        if(pc.channel_mode is not None):
            pc.delete()
        self.assertIsNone(pc.trunk)

    def test_trunk_write(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        oldtrunk = pc.trunk
        for trunk in self.trunk_values:
            pc.trunk = trunk
            self.assertEqual(trunk,pc.trunk)
        pc.trunk = oldtrunk
        pc.delete()

    def test_trunk_write_invalid(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        trunk = "asdf"
        with self.assertRaises(CLIError) as e:
            pc.trunk = trunk
        self.assertEqual("The command \" interface port-channel"+str(i)+" ; switchport trunk mode  "+str(trunk)+" \" gave the error \" % Invalid command \".",str(e.exception))
        pc.delete()

