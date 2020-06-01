import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrAnalytics(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    # def test_analytics_read(self):
    #     log.debug("Analytics : " + str(self.switch.analytics))
    #     self.skipTest("Needs to be fixed" + self.switch.analytics)

    def test_analytics_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.analytics = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
