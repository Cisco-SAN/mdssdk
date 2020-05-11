import unittest

from mdssdk.fc import Fc
from mdssdk.connection_manager.errors import CLIError


class TestFcAttrDescription(unittest.TestCase):

    def test_description_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        self.assertIsNotNone(fc.description)

    def test_description_write_max254(self):
        fc = Fc(self.switch, self.fc_name[1])
        old = fc.description
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch123456789123456789123456"
        fc.description = desc
        self.assertEqual(desc, fc.description)
        fc.description = old

    def test_description_write_beyondmax(self):
        fc = Fc(self.switch, self.fc_name[2])
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678"
        with self.assertRaises(CLIError) as e:
            fc.description = desc
        self.assertEqual("The command \" interface " + str(self.fc_name[2]) + " ; switchport description  " + str(
            desc) + " \" gave the error \" % String exceeded max length of (254) \".", str(e.exception))
