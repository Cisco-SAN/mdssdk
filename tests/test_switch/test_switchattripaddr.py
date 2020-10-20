import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrIpAddr(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.ip_address = ip_address

    def test_ipaddr_read(self):
        self.assertEqual(self.ip_address, self.switch.ipaddr)

    def test_ipaddr_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.ipaddr = "10.197.155.244"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
