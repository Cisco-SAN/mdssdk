import unittest

from mdssdk.connection_manager.errors import CLIError
from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchConfig(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.commands = "vsan database ; vsan 2 ; terminal dont-ask ; no vsan 2 ; no terminal dont-ask"
        self.commands_clierror = "terminal dont-ask ; vsan database ; no vsan 2 "

    def test_config(self):
        out = self.switch.config(self.commands)
        log.debug("Result of config : " + str(self.commands) + "\n" + str(out))
        self.assertFalse(out)

    def test_config_error(self):
        with self.assertRaises(CLIError) as e:
            self.switch.config(self.commands_clierror)
        log.debug(
            "Config : " + str(self.commands_clierror) + " raises " + str(e.exception)
        )

    def tearDown(self) -> None:
        pass
