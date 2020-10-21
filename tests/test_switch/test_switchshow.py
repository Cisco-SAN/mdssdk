import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchShow(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.commands = "show vsan usage"

    def test_show(self):
        log.debug("Output of show : " + str(self.commands))
        log.debug(self.switch.show(self.commands))
        self.skipTest("Needs to be fixed")

    def test_show_rawtext(self):
        log.debug("Output of show(raw text) : " + str(self.commands))
        log.debug(self.switch.show(self.commands, True))
        self.skipTest("Needs to be fixed")

    def tearDown(self) -> None:
        pass
