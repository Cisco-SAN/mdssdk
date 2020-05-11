import unittest

from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError


class TestFcAttrStatus(unittest.TestCase):

    def test_status_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        self.assertIsNotNone(fc.status)

    def test_status_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        if (fc.status == "sfpAbsent"):
            return
        status = "shutdown"
        fc.status = status
        self.assertEqual("down", fc.status)
        status1 = "no shutdown"
        fc.status = status1
        self.assertIn(fc.status, self.status_values)

    def test_status_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        status = "asdf"
        with self.assertRaises(CLIError) as e:
            fc.status = status
        self.assertEqual("The command \" terminal dont-ask ; interface " + str(fc.name) + " ; " + str(
            status) + " ; no terminal dont-ask \" gave the error \" % Invalid command \".", str(e.exception))
