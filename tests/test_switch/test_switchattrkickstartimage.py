import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrKickstartImage(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_kickstart_image_read(self):
        print("Kickstart Image : " + str(self.switch.kickstart_image))
        self.skipTest("need to fix")

    def test_kickstart_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.kickstart_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
