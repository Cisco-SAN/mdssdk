import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrModules(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

    def test_modules_read(self):
        if (self.switch.modules is not None):
            log.debug("Modules : ")
            for modobj in self.switch.modules.values():
                temp = [x for x in dir(modobj) if not x.startswith('_')]
                for t in temp:
                    v = modobj.__getattribute__(t)
                    self.assertIsNotNone(v)
                    log.debug(str(t) + " : " + str(v))
        else:
            self.fail("switch.modules failed to get module objects")

    def test_modules_write_error(self):
        if (self.switch.modules is not None):
            with self.assertRaises(AttributeError) as e:
                list(self.switch.modules.values())[0].module_number = 5
            self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
