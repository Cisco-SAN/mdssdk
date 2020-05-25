import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrCores(unittest.TestCase):
   
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
    
    def test_cores_read(self):
        print("Cores " + str(self.switch.cores))
        self.skipTest("need to fix")

    def test_cores_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.cores = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass