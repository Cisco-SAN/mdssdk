import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)

class TestSwitchAttrModules(unittest.TestCase):
    
    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)

    def test_modules_read(self):
        if (self.switch.modules is not None):
            print("Modules : ")
            temp = [x for x in dir(self.switch.modules[0]) if not x.startswith('_')]
            for t in temp:
                print(str(t) + " : " + str(self.switch.modules[0].__getattribute__(t)))
        else:
            print("Modules : None")

    def test_modules_write_error(self):
        if (self.switch.modules is not None):
            with self.assertRaises(AttributeError) as e:
                self.switch.modules[0].module_number = 5
            self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
