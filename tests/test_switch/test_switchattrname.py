import re
import unittest

from mdssdk.connection_manager.errors import CLIError
from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrName(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.oldname = self.switch.name
        self.oldname_without_domain = re.sub("\.cisco\.com", "", self.oldname)

    def test_name_read(self):
        swname = self.switch.name
        log.debug("Switch Name : " + swname)
        self.assertRegex(swname, "^\S+$", msg="Switch name not correct")

    def test_name_write_max32(self):
        name = "switch12345678912345678912345678"
        self.switch.name = name
        swname = re.sub("\.cisco\.com", "", self.switch.name)
        # Move to old name
        self.switch.name = self.oldname_without_domain
        # Later check
        self.assertEqual(name, swname)

    def test_name_write_beyondmax(self):
        name = "switch123456789123456789123456789"
        with self.assertRaises(CLIError) as e:
            self.switch.name = name
        self.assertEqual(
            'The command " switchname '
            + str(name)
            + ' " gave the error " % String exceeded max length of (32) ".',
            str(e.exception),
        )

    def test_name_write_invalid(self):
        name = "1switch"
        with self.assertRaises(CLIError) as e:
            self.switch.name = name
        self.assertIn(
            "Invalid switch name. Must start with a letter, end with alphanumeric",
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.switch.name = self.oldname_without_domain
        self.assertEqual(self.oldname, self.switch.name)
