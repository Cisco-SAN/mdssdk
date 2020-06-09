import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrNpv(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_npv_read(self):
        self.assertIn(self.switch.npv, [True, False])

    def test_npv_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.npv = True
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
