import unittest

from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrCounters(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        interfaces = sw.interfaces
        while True:
            k,v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.info(k)
                break 

    def test_counters_read(self):
        dir_counters = [x for x in dir(self.fc.counters) if not x.startswith('_')]
        print("Counters "+str(self.fc.name))
        for t in dir_counters:
            print(str(t) + " : " + str(self.fc.counters.__getattribute__(t)))
        self.skipTest("need to fix assertion")

    def test_counters_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.counters = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def test_counters_clear(self):
        self.skipTest("needs to fix")
        self.fc.counters.clear()

    def tearDown(self) -> None:
        pass