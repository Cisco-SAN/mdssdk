import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrKickstartImage(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_kickstart_image_read(self):
        ki = self.switch.kickstart_image
        log.debug("Kickstart Image : " + str(ki))
        self.assertRegex(ki, "bootflash\S+", "Kickstart image is not correct")

    def test_kickstart_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.kickstart_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def test_system_image_read(self):
        si = self.switch.kickstart_image
        log.debug("System Image : " + str(si))
        self.assertRegex(si, "bootflash\S+", "System image is not correct")

    def test_system_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.system_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
