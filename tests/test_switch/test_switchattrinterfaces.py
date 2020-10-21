import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrInterfaces(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_interfaces_read(self):
        interfaces = self.switch.interfaces
        self.assertIsInstance(interfaces, dict, "Interfaces is not of correct type")
        self.assertIsNotNone(interfaces, "Interfaces cannot be None")

    def test_interfaces_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.interfaces = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
