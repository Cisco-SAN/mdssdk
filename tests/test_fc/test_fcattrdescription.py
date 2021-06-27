import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrDescription(unittest.TestCase):
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
        self.old = self.fc.description

    def test_description_read(self):
        self.assertIsNotNone(self.fc.description)

    def test_description_write_max254(self):
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch123456789123456789123456"
        self.fc.description = desc
        self.assertEqual(desc, self.fc.description)
        self.fc.description = self.old
        self.assertEqual(self.old, self.fc.description)

    def test_description_write_beyondmax(self):
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678"
        with self.assertRaises(CLIError) as e:
            self.fc.description = desc
        self.assertIn("String exceeded max length of (254)", str(e.exception))

    def tearDown(self) -> None:
        self.fc.description = self.old
        self.assertEqual(self.old, self.fc.description)
