import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrVersion(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_version_read(self):
        log.debug("Version : " + str(self.switch.version))
        self.skipTest("Needs to be fixed")

    def test_version_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.version = '8.4'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
