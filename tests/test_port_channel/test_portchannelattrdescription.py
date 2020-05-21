import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel


class TestPortChannelAttrDescription(unittest.TestCase):

    def test_description_read(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        self.assertIsNotNone(pc.description)
        pc.delete()

    def test_description_read_nonexisting(self):
        i = self.pc_id[1]
        pc = PortChannel(self.switch, i)
        if(pc.channel_mode is not None):
            pc.delete()
        with self.assertRaises(CLIError) as e:
            print(pc.description)
        self.assertIn("Invalid range", str(e.exception))

    def test_description_write_max254(self):
        pc = PortChannel(self.switch, self.pc_id[2])
        pc.create()
        old = pc.description
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch123456789123456789123456"
        pc.description = desc
        self.assertEqual(desc, pc.description)
        pc.description = old
        pc.delete()

    def test_description_write_beyondmax(self):
        i = self.pc_id[3]
        pc = PortChannel(self.switch, i)
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678"
        with self.assertRaises(CLIError) as e:
            pc.description = desc
        self.maxDiff = None
        self.assertEqual("The command \" interface port-channel"+str(i)+" ; switchport description  switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678 \" gave the error \" % String exceeded max length of (254) \".",str(e.exception))

    


