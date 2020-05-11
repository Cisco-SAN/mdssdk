import unittest

from mdssdk.portchannel import PortChannel,PortChannelNotPresent,InvalidChannelMode

class TestPortChannelAttrChannelMode(unittest.TestCase):

    def test_channel_mode_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        self.assertIsNone(pc.channel_mode)

    def test_channel_mode_read(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        self.assertIn(pc.channel_mode, self.channel_mode)
        pc.delete()

    def test_channel_mode_write_nonexisting(self):
        id = self.pc_id[2]
        pc = PortChannel(self.switch, id)
        with self.assertRaises(PortChannelNotPresent) as e:
            pc.channel_mode = self.channel_mode[0]
        self.assertEqual("PortChannelNotPresent: Port channel " + str(id) + " is not present on the switch, please create the PC first",str(e.exception))

    def test_channel_mode_write(self):
        id = self.pc_id[3]
        pc = PortChannel(self.switch, id)
        pc.create()
        for mode in self.channel_mode:
            pc.channel_mode = mode
            self.assertEqual(mode,pc.channel_mode)
        pc.delete()

    def test_channel_mode_write_invalid(self):
        id = self.pc_id[4]
        channel_mode = "asdf"
        pc = PortChannel(self.switch, id)
        pc.create()
        with self.assertRaises(InvalidChannelMode) as e:
            pc.channel_mode = channel_mode
        self.assertEqual("InvalidChannelMode: Invalid channel mode ("+str(channel_mode)+"), Valid values are: on,active",str(e.exception))
        pc.delete()
