import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchReload(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_reload(self):
        self.skipTest("Skipping Reload, Needs to be fixed")
        log.debug(self.switch.reload())

    def tearDown(self) -> None:
        pass
