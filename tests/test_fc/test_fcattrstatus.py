import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrStatus(unittest.TestCase):
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
        self.old = self.fc.status
        self.status_values = status_values

    def test_status_read(self):
        self.assertIn(self.fc.status, self.status_values)

    def test_status_write(self):
        self.skipTest("needs to be fixed")
        if self.fc.status == "down":
            self.fc.status = "no shutdown"
            self.assertIn(self.fc.status, self.status_values)
            status = "shutdown"
            self.fc.status = status
            self.assertEqual(self.old, self.fc.status)
        else:
            status = "shutdown"
            self.fc.status = status
            self.assertEqual("down", self.fc.status)
            self.fc.status = "no shutdown"
            self.assertEqual(self.old, self.fc.status)

    def test_status_write_invalid(self):
        status = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.status = status
        self.assertEqual(
            'The command " terminal dont-ask ; interface '
            + self.fc.name
            + " ; "
            + str(status)
            + ' ; no terminal dont-ask " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.assertEqual(self.old, self.fc.status)
