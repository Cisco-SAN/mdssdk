import unittest

from mdssdk.portchannel import PortChannel

class TestPortChannelAttrName(unittest.TestCase):

    def test_name_read(self):
        i = self.pc_id[0]
        pc = PortChannel(self.switch, i)
        pc.create()
        self.assertEqual('port-channel'+str(i),pc.name)
        pc.delete()

    def test_name_write_error(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        with self.assertRaises(AttributeError) as e:
            pc.name = "asdf"
        self.assertEqual("can't set attribute",str(e.exception))
