import unittest

from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError


class TestFcAttrMode(unittest.TestCase):

    def test_mode_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        self.assertIsNotNone(fc.mode)

    def test_mode_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        oldmode = fc.mode
        for mode in self.modes_allowed:
            fc.mode = mode
            self.assertEqual(mode, fc.mode)
        if ('--' in oldmode):
            oldmode = 'auto'
        fc.mode = oldmode

    def test_mode_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        mode = "asdf"
        with self.assertRaises(CLIError) as e:
            fc.mode = mode
        self.assertEqual("The command \" interface " + str(self.fc_name[2]) + " ; switchport mode  " + str(
            mode) + " \" gave the error \" % Invalid command \".", str(e.exception))
