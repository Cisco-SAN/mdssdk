import unittest
import random

from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrTransceiver(unittest.TestCase):
    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        interfaces = sw.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if type(v) is Fc:
                self.fc = v
                log.debug(k)
                break

    def test_transceiver_read(self):
        dir_trans = [x for x in dir(self.fc.transceiver) if not x.startswith("_")]
        log.debug(str(self.fc.name) + " transceiver : ")
        for t in dir_trans:
            log.debug(str(t) + " : " + str(self.fc.transceiver.__getattribute__(t)))
        self.skipTest("needs to be fixed")

    def test_transceiver_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.transceiver = []
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
