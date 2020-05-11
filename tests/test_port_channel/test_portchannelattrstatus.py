import unittest

from mdssdk.portchannel import PortChannel
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelAttrStatus(unittest.TestCase):

    def test_status_read(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        self.assertIsNotNone(pc.status)
        pc.delete()

    def test_status_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        if(pc.channel_mode is not None):
            pc.delete()
        self.assertIsNone(pc.status)

    def test_status_write(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        status = "shutdown"
        pc.status = status
        self.assertEqual("down", pc.status)
        status1 = "no shutdown"
        pc.status = status1
        self.assertEqual("noOperMembers", pc.status)
        pc.delete()

    def test_status_write_invalid(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        status = "asdf"
        with self.assertRaises(CLIError) as e:
            pc.status = status
        self.assertEqual("The command \" terminal dont-ask ; interface port-channel"+str(i)+" ; "+str(status)+" ; no terminal dont-ask \" gave the error \" % Invalid command \".",str(e.exception))
        pc.delete()

