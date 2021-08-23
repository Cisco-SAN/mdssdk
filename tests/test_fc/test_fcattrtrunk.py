import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrTrunk(unittest.TestCase):
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
        self.trunk_values = trunk_values
        self.old = self.fc.trunk

    def test_trunk_read(self):
        self.assertIn(self.fc.trunk, self.trunk_values + ["--"])

    def test_trunk_write(self):
        for trunk in self.trunk_values:
            try:
                self.fc.trunk = trunk
            except CLIError as c:
                if "port already in a port-channel, no config allowed" in c.message:
                    self.skipTest(
                        "Skipping test as port already in a port-channel, no config allowed"
                    )
            self.assertEqual(trunk, self.fc.trunk)
        self.fc.trunk = self.old
        self.assertEqual(self.old, self.fc.trunk)

    def test_trunk_write_invalid(self):
        trunk = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.trunk = trunk
        self.assertEqual(
            'The command " interface '
            + str(self.fc.name)
            + " ; switchport trunk mode  "
            + str(trunk)
            + ' " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        if self.fc.trunk != self.old:
            self.fc.trunk = self.old
            self.assertEqual(self.old, self.fc.trunk)
