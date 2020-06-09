import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrIpAddr(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.ip_address = ip_address

    def test_ipaddr_read(self):
        self.assertEqual(self.ip_address, self.switch.ipaddr)

    def test_ipaddr_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.ipaddr = '10.197.155.244'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
