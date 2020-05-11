import unittest
from mdssdk.connection_manager.errors import CLIError


class TestSwitchAttrName(unittest.TestCase):
    # name - rw
    def test_name_read(self):
        print("Switch Name : " + str(self.switch.name))

    def test_name_write_max32(self):
        oldname = self.switch.name
        name = self.name_max32
        self.switch.name = name
        self.assertEqual(name, self.switch.name)
        self.switch.name = oldname

    def test_name_write_beyondmax(self):
        name = self.name_beyondmax
        with self.assertRaises(CLIError) as e:
            self.switch.name = name
        self.assertEqual(
            "The command \" switchname " + str(name) + " \" gave the error \" % String exceeded max length of (32) \".",
            str(e.exception))

    def test_name_write_invalid(self):
        name = self.invalid_name  # starts with digit
        with self.assertRaises(CLIError) as e:
            self.switch.name = name
        self.assertEqual("The command \" switchname " + str(
            name) + " \" gave the error \" Invalid switch name. Must start with a letter, end with alphanumeric\nand contain alphanumeric and hyphen only \".",
                         str(e.exception))
