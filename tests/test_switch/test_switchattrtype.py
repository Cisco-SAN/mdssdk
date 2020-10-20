import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrType(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_type_read(self):
        type = str(self.switch.type)
        log.debug("Type : " + type)
        self.assertIsNotNone(type)

    def test_type_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.type = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
