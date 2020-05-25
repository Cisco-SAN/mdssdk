import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchReload(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_reload(self):
        self.skipTest("Skipping Reload")
        print(self.switch.reload())

    def tearDown(self) -> None:
        pass