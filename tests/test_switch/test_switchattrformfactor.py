import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrFormFactor(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_form_factor_read(self):
        print("Form Factor : " + str(self.switch.form_factor))
        self.skipTest("need to fix")

    def test_form_factor_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.form_factor = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
