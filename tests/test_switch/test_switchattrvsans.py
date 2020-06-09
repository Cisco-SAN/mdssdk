import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrVsans(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_vsans_read(self):
        log.debug("Vsans : " + str(self.switch.vsans))
        self.skipTest("Needs to be fixed")

    def test_vsans_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.vsans = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
