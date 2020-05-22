import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrVersion(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_version_read(self):
        print("Version : " + str(self.switch.version))

    def test_version_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.version = '8.4'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
