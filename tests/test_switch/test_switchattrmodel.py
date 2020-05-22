import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrModel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_model_read(self):
        print("Model : " + str(self.switch.model))

    def test_model_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.model = 'mds'
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
    	pass
