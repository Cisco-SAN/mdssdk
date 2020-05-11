import unittest

from mdssdk.portchannel import PortChannel

class TestPortChannelAttrId(unittest.TestCase):

    def test_id_read(self):
        i = self.pc_id[0]
        pc = PortChannel(self.switch, i)
        self.assertEqual(i,pc.id)

    def test_id_write_error(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        with self.assertRaises(AttributeError) as e:
            pc.id = 2
        self.assertEqual("can't set attribute",str(e.exception))
