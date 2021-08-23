import random
import unittest

from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrCounters(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        interfaces = self.switch.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if type(v) is Fc:
                self.fc = v
                log.debug(k)
                break

    def test_counters_read(self):
        dir_counters = [x for x in dir(self.fc.counters) if not x.startswith("_")]
        log.debug("Counters " + str(self.fc.name))
        for t in dir_counters:
            log.debug(str(t) + " : " + str(self.fc.counters.__getattribute__(t)))
        self.assertIsNotNone(
            self.fc.counters, "fc.counters did not get counter objects"
        )

    def test_counters_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.counters = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def test_counters_clear(self):
        self.skipTest("needs to fix")
        self.fc.counters.clear()

    def tearDown(self) -> None:
        pass
