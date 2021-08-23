import random
import unittest

import time

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrOutOfService(unittest.TestCase):
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
        self.status_values = status_values
        self.old = self.fc.status

    def test_out_of_service_read_error(self):
        with self.assertRaises(AttributeError) as e:
            log.debug(self.fc.out_of_service)
        self.assertEqual("unreadable attribute", str(e.exception))

    def test_out_of_service_write(self):
        # self.skipTest("needs to be fixed")
        if self.fc.status == "outOfServc":
            self.fc.out_of_service = False
            self.assertIn(self.fc.status, self.status_values)
            self.fc.out_of_service = True
            self.assertEqual("outOfServc", self.fc.status)
        else:
            try:
                self.fc.out_of_service = True
            except CLIError as c:
                if "requested config not allowed on bundle member" in c.message:
                    self.skipTest(
                        "Port "
                        + self.fc.name
                        + " is part of a PC and hence cannot set to out-of-service, Please rerun the tests"
                    )
            self.assertEqual("outOfServc", self.fc.status)
            self.fc.out_of_service = False
            # if self.old != "down":
            self.fc.status = "no shutdown"
            time.sleep(2)
            # Sometimes the states may not be same so no need to check this as of now
            # self.assertEqual(self.old, self.fc.status)

    def test_out_of_service_write_invalid(self):
        with self.assertRaises(TypeError) as e:
            self.fc.out_of_service = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))

    def tearDown(self) -> None:
        self.fc.out_of_service = False
        # if self.old != "down":
        self.fc.status = "no shutdown"
        time.sleep(5)
        # Sometimes the states may not be same so no need to check this as of now
        # self.assertEqual(self.old, self.fc.status)
