import unittest

from mdssdk.portchannel import PortChannel,InvalidPortChannelRange

class TestPortChannelCreate(unittest.TestCase):

    def test_create(self):
        pc = PortChannel(self.switch, self.pc_id)
        pc.create()
        self.assertEqual(self.pc_id,pc.id)
        pc.delete()

    def test_create_max(self):
        for i in self.valid_pc_id:
            pc = PortChannel(self.switch, i)
            pc.create()
            self.assertEqual(i,pc.id)
        for i in self.valid_pc_id:
            pc = PortChannel(self.switch, i)
            pc.delete()


    def test_create_invalid(self):
        for i in self.invalid_pc_id:
            with self.assertRaises(InvalidPortChannelRange) as e:
                pc = PortChannel(self.switch, i)
            self.assertEqual("InvalidPortChannelRange: Port channel id " + str(i) + " is invalid, id should range from 1 to 256",str(e.exception))



