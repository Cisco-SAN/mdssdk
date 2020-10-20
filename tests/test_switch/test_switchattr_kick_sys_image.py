import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrKickstartImage(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_kickstart_image_read(self):
        ki = self.switch.kickstart_image
        log.debug("Kickstart Image : " + str(ki))
        self.assertRegex(ki, "bootflash\S+", "Kickstart image is not correct")

    def test_kickstart_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.kickstart_image = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def test_system_image_read(self):
        si = self.switch.kickstart_image
        log.debug("System Image : " + str(si))
        self.assertRegex(si, "bootflash\S+", "System image is not correct")

    def test_system_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.system_image = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
