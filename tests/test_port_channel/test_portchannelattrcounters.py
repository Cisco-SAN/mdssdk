import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from mdssdk.fc import Fc

class TestPortChannelAttrCounters(unittest.TestCase):

    def test_counters_read_nonexisting(self):
        i = self.pc_id[0]
        pc = PortChannel(self.switch, i)
        print(pc.counters)
        with self.assertRaises(CLIError) as e:
            print(pc.counters.__getattribute__('brief'))
        self.assertEqual('The command " show interface port-channel'+str(i)+' counters brief " gave the error " Invalid range ".',str(e.exception))
        pc.delete()

    def test_counters_read(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        temp = [x for x in dir(pc.counters) if not x.startswith('_')]
        for t in temp:
            print(str(t)+" "+str(pc.counters.__getattribute__(t)))
        pc.delete()

    def test_counters_write_error(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        with self.assertRaises(AttributeError) as e:
            pc.counters = "mds"
        self.assertEqual("can't set attribute",str(e.exception))
