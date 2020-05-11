import unittest

from mdssdk.portchannel import PortChannel
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelAttrMode(unittest.TestCase):

    def test_mode_read(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        self.assertIsNotNone(pc.mode)
        pc.delete()

    def test_mode_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        if(pc.channel_mode is not None):
            pc.delete()
        self.assertIsNone(pc.mode)

    def test_mode_write(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        oldmode = pc.mode
        for mode in self.modes_allowed:
            pc.mode = mode
            self.assertEqual(mode,pc.mode)
        if('--' in oldmode):
            oldmode = 'auto'
        pc.mode = oldmode
        pc.delete()

    def test_mode_write_invalid(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        mode = "asdf"
        with self.assertRaises(CLIError) as e:
            pc.mode = mode
        self.assertEqual("The command \" interface port-channel"+str(i)+" ; switchport mode  "+str(mode)+" \" gave the error \" % Invalid command \".",str(e.exception))
       

