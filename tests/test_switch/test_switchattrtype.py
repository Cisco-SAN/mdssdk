import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrType(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_type_read(self):
        print("Type : " + str(self.switch.type))

    def test_type_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.type = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
