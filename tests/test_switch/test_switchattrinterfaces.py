import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrInterfaces(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_interfaces_read(self):
        print("Interfaces : " + str(self.switch.interfaces))
        self.skipTest("need to fix")

    def test_interfaces_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.interfaces = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
