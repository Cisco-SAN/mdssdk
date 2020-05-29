import unittest

from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrTransceiver(unittest.TestCase):

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

    def test_transceiver_read(self):
        dir_trans = [x for x in dir(self.fc.transceiver) if not x.startswith('_')]
        print(str(self.fc.name) + " transceiver : ")
        for t in dir_trans:
            print(str(t) + " : " + str(self.fc.transceiver.__getattribute__(t)))
        self.skipTest("needs to be fixed")
             
    def test_transceiver_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.transceiver = []
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass