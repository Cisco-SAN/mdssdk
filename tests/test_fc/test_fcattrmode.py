import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrMode(unittest.TestCase):

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
        self.old = self.fc.mode
        self.mode_values = mode_values

    def test_mode_read(self):
        self.assertIn(self.fc.mode, self.mode_values + ['TE', 'TF', '--', ' --'])

    def test_mode_write(self):
        self.skipTest("needs to be fixed")
        for mode in self.mode_values:
            self.fc.mode = mode
            self.assertEqual(mode, self.fc.mode)

    def test_mode_write_invalid(self):
        mode = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.mode = mode
        self.assertEqual("The command \" interface " + self.fc.name + " ; switchport mode  " + str(
            mode) + " \" gave the error \" % Invalid command \".", str(e.exception))

    def tearDown(self) -> None:
        if(self.fc.mode != self.old):
            if ("--" in self.old):
                self.fc.mode = 'auto'
            elif self.fc.mode == 'TE':
                self.fc.mode = 'E'
            elif self.fc.mode == 'TF':
                self.fc.mode = 'F'   
            else:
                self.fc.mode = self.old
            self.assertEqual(self.old, self.fc.mode)