import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrAnalytics(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_analytics_read(self):
        print("Analytics : " + str(self.switch.analytics))
        self.skipTest("need to fix")

    def test_analytics_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.analytics = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass