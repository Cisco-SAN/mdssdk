import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrTrunk(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        interfaces = sw.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.debug(k)
                break
        self.trunk_values = trunk_values
        self.old = self.fc.trunk

    def test_trunk_read(self):
        self.assertIn(self.fc.trunk, self.trunk_values)

    def test_trunk_write(self):
        for trunk in self.trunk_values:
            self.fc.trunk = trunk
            self.assertEqual(trunk, self.fc.trunk)
        self.fc.trunk = self.old
        self.assertEqual(self.old, self.fc.trunk)

    def test_trunk_write_invalid(self):
        trunk = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.trunk = trunk
        self.assertEqual("The command \" interface " + str(self.fc.name) + " ; switchport trunk mode  " + str(
            trunk) + " \" gave the error \" % Invalid command \".", str(e.exception))

    def tearDown(self) -> None:
        self.fc.trunk = self.old
        self.assertEqual(self.old, self.fc.trunk)