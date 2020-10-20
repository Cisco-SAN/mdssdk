import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrImageString(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_image_string_read(self):
        imgstr = self.switch.image_string
        log.debug("Image String : " + str(imgstr))
        self.assertRegex(imgstr, "m9.*")

    def test_image_string_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.image_string = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
