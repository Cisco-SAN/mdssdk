import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrNpv(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_npv_read(self):
        self.assertIn(self.switch.npv, [True, False])

    def test_npv_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.npv = True
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
