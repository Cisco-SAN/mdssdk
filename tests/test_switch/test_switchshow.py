import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchShow(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        self.commands = "show vsan usage"

    def test_show(self):
        print("Output of show : " + str(self.commands))
        print(self.switch.show(self.commands))
        self.skipTest("need to fix")

    def test_show_rawtext(self):
        print("Output of show(raw text) : " + str(self.commands))
        print(self.switch.show(self.commands, True))
        self.skipTest("need to fix")

    def tearDown(self) -> None:
        pass
