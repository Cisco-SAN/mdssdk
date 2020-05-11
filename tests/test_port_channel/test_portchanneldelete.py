import unittest

from mdssdk.portchannel import PortChannel

class TestPortChannelDelete(unittest.TestCase):

    def test_delete_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.delete()
        self.assertIsNone(pc.channel_mode)

    def test_delete(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        self.assertIsNotNone(pc.channel_mode)
        pc.delete()
        self.assertIsNone(pc.channel_mode)



