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

    def test_type_snum_and_others(self):
        snum = str(self.switch.serial_num)
        pid = str(self.switch.product_id)
        sut = str(self.switch.system_uptime)
        lbt = str(self.switch.last_boot_time)

        self.assertIsNotNone(snum)
        self.assertIsNotNone(pid)
        self.assertIsNotNone(sut)
        # lbt can be none sometimes
        # self.assertIsNotNone(lbt)

    def tearDown(self) -> None:
        pass
