import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrVersion(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_version_read(self):
        v = str(self.switch.version)
        log.debug("Version : " + v)
        self.assertIsNotNone(v)

    def test_version_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.version = "8.4"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
