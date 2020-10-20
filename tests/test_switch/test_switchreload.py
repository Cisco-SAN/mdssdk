import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchReload(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_reload(self):
        self.skipTest("Skipping Reload, Needs to be fixed")
        log.debug(self.switch.reload())

    def tearDown(self) -> None:
        pass
