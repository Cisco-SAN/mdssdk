import unittest

from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError


class TestFcAttrSpeed(unittest.TestCase):

    def test_speed_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        # print(fc.speed)
        self.assertIsNotNone(fc.speed)

    def test_speed_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        oldspeed = fc.speed
        for speed in self.speeds_allowed:
            fc.speed = speed
            self.assertEqual(speed, fc.speed)
        if ("--" in oldspeed):
            oldspeed = 'auto'
        fc.speed = oldspeed

    def test_speed_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        speed = "asdf"
        with self.assertRaises(CLIError) as e:
            fc.speed = speed
        self.assertEqual("The command \" interface " + str(fc.name) + " ; switchport speed  " + str(
            speed) + " \" gave the error \" % Invalid command \".", str(e.exception))
