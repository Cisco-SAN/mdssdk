import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrMode(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        interfaces = self.switch.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if type(v) is Fc:
                self.fc = v
                log.debug(k)
                break
        self.old = self.fc.mode
        self.mode_values = mode_values

    def test_mode_read(self):
        self.assertIn(self.fc.mode, self.mode_values + ["TE", "TF", "TNP", "--", " --"])

    def test_mode_write(self):
        try:
            self.fc.mode = "auto"
        except CLIError as c:
            if "requested config not allowed on bundle member" in c.message:
                self.skipTest(
                    "Port "
                    + self.fc.name
                    + " is part of a PC and hence cannot set mode to auto, Please rerun the tests"
                )
        self.assertIn(self.fc.mode, self.mode_values + ["TE", "TF", "TNP", "--", " --"])

    def test_mode_write_invalid(self):
        mode = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.mode = mode
        self.assertEqual(
            'The command " interface '
            + self.fc.name
            + " ; switchport mode  "
            + str(mode)
            + ' " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        if self.fc.mode != self.old:
            if "--" in self.old:
                self.fc.mode = "auto"
            elif self.fc.mode == "TE":
                self.fc.mode = "E"
            elif self.fc.mode == "TF":
                self.fc.mode = "F"
            else:
                self.fc.mode = self.old
            self.assertEqual(self.old, self.fc.mode)
