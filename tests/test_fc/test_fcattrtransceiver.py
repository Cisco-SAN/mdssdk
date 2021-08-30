import random
import unittest

from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrTransceiver(unittest.TestCase):
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
                if self.fc.transceiver.sfp_present:
                    log.debug(k)
                    break

    def test_transceiver_read(self):
        self.assertIsNotNone(
            self.fc.transceiver, "fc.transceiver did not get transceiver objects"
        )
        dir_trans = [x for x in dir(self.fc.transceiver) if not x.startswith("_")]
        log.debug(str(self.fc.name) + " transceiver : ")
        for t in dir_trans:
            log.debug(str(t) + " : " + str(self.fc.transceiver.__getattribute__(t)))
        # self.skipTest("needs to be fixed")

    def test_transceiver_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.transceiver = []
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
