import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrType(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_type_read(self):
        log.debug("Type : " + str(self.switch.type))
        self.skipTest("Needs to be fixed")

    def test_type_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.type = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
