import unittest

from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrName(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        interfaces = sw.interfaces
        while True:
            k,v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                self.name = k
                break
        log.info(self.name)

    def test_name_read(self):
        self.assertEqual(self.name, self.fc.name)

    def test_name_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.fc.name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass