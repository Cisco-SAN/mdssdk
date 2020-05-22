import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrNpv(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_npv_read(self):
        print("Npv switch : " + str(self.switch.npv))

    def test_npv_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.npv = True
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
