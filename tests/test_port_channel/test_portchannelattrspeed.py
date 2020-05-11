import unittest

from mdssdk.portchannel import PortChannel
from mdssdk.connection_manager.errors import CLIError

class TestPortChannelAttrSpeed(unittest.TestCase):

    def test_speed_read(self):
        pc = PortChannel(self.switch, self.pc_id[0])
        pc.create()
        self.assertIsNotNone(pc.speed)
        pc.delete()

    def test_speed_read_nonexisting(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        if(pc.channel_mode is not None):
            pc.delete()
        self.assertIsNone(pc.speed)

    def test_speed_write(self):
        pc = PortChannel(self.switch, self.pc_id[1])
        pc.create()
        oldspeed = pc.speed
        for speed in self.speeds_allowed:
            pc.speed = speed
            self.assertEqual(speed, pc.speed)  
        if('--' in oldspeed):
            oldspeed = 'auto'
        pc.speed = oldspeed

    def test_speed_write_invalid(self):
        i = self.pc_id[2]
        pc = PortChannel(self.switch, i)
        speed = "asdf"
        with self.assertRaises(CLIError) as e:
            pc.speed = speed
        self.assertEqual("The command \" interface port-channel"+str(i)+" ; switchport speed  "+str(speed)+" \" gave the error \" % Invalid command \".",str(e.exception))
