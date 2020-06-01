import unittest

from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrModules(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_modules_read(self):
        if (self.switch.modules is not None):
            log.debug("Modules : ")
            temp = [x for x in dir(self.switch.modules[0]) if not x.startswith('_')]
            for t in temp:
                log.debug(str(t) + " : " + str(self.switch.modules[0].__getattribute__(t)))
        else:
            log.debug("Modules : None")
        self.skipTest("Needs to be fixed")

    def test_modules_write_error(self):
        if (self.switch.modules is not None):
            with self.assertRaises(AttributeError) as e:
                self.switch.modules[0].module_number = 5
            self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
