import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrImageString(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_image_string_read(self):
        imgstr = self.switch.image_string
        log.debug("Image String : " + str(imgstr))
        self.assertRegex(imgstr, "m9.*")

    def test_image_string_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.image_string = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
