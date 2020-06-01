import unittest

from mdssdk.connection_manager.errors import CLIError
from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchConfig(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.commands = "vsan database ; vsan 2 ; terminal dont-ask ; no vsan 2 ; no terminal dont-ask"
        self.commands_clierror = "terminal dont-ask ; vsan database ; no vsan 2 "

    def test_config(self):
        out = self.switch.config(self.commands)
        log.debug("Result of config : " + str(self.commands) + "\n" + str(out))
        self.assertFalse(out)

    def test_config_error(self):
        with self.assertRaises(CLIError) as e:
            self.switch.config(self.commands_clierror)
        log.debug("Config : " + str(self.commands_clierror) + " raises " + str(e.exception))

    def tearDown(self) -> None:
        pass
