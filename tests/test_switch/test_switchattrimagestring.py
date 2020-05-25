import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrImageString(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_image_string_read(self):
        print("Image String : " + str(self.switch.image_string))
        self.skipTest("need to fix")

    def test_image_string_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.image_string = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
