import unittest

from mdssdk.fc import Fc
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrOutOfService(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        interfaces = sw.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.debug(k)
                break
        self.status_values = status_values
        self.old = self.fc.status

    def test_out_of_service_read_error(self):
        with self.assertRaises(AttributeError) as e:
            log.debug(self.fc.out_of_service)
        self.assertEqual("unreadable attribute", str(e.exception))

    def test_out_of_service_write(self):
        self.skipTest("needs to be fixed")
        if(self.fc.status == 'outOfServc'):
            self.fc.out_of_service = False
            self.assertIn(self.fc.status, self.status_values)
            self.fc.out_of_service = True
            self.assertEqual('outOfServc', self.fc.status)
        else:
            self.fc.out_of_service = True
            self.assertEqual('outOfServc', self.fc.status)
            self.fc.out_of_service = False
            self.assertEqual(self.old, self.fc.status)

    def test_out_of_service_write_invalid(self):
        with self.assertRaises(TypeError) as e:
            self.fc.out_of_service = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))

    def tearDown(self) -> None:
        self.assertEqual(self.old, self.fc.status)