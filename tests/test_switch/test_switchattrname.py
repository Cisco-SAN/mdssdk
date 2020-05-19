import re
import unittest

from mdssdk.connection_manager.errors import CLIError


class TestSwitchAttrName(unittest.TestCase):
    # name - rw
    def test_name_read(self):
        print("Switch Name : " + self.switch.name)

    def test_name_write_max32(self):
        oldname = self.switch.name
        oldname_without_domain = re.sub('\.cisco\.com', '', oldname)
        print("Switch OLD Name : " + oldname)
        name = self.name_max32
        self.switch.name = name
        swname = re.sub('\.cisco\.com', '', self.switch.name)
        # Move to old name
        self.switch.name = oldname_without_domain
        # Later check
        self.assertEqual(name, swname)

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
            self.assertIn("Invalid switch name. Must start with a letter, end with alphanumeric", str(e.exception))
