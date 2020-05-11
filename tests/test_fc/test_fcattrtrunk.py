import unittest

from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError


class TestFcAttrTrunk(unittest.TestCase):

    def test_trunk_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        self.assertIn(fc.trunk, self.trunk_values)

    def test_trunk_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        oldtrunk = fc.trunk
        for trunk in self.trunk_values:
            fc.trunk = trunk
            self.assertEqual(trunk, fc.trunk)
        fc.trunk = oldtrunk

    def test_trunk_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        trunk = "asdf"
        with self.assertRaises(CLIError) as e:
            fc.trunk = trunk
        self.assertEqual("The command \" interface " + str(fc.name) + " ; switchport trunk mode  " + str(
            trunk) + " \" gave the error \" % Invalid command \".", str(e.exception))
