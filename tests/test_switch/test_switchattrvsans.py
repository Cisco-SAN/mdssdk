import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrVsans(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_vsans_read(self):
        print("Vsans : " + str(self.switch.vsans))
        self.skipTest("need to fix")

    def test_vsans_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.vsans = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
