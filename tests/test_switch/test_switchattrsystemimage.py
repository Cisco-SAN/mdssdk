import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrSystemImage(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_system_image_read(self):
        print("System Image : " + str(self.switch.system_image))

    def test_system_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.system_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
