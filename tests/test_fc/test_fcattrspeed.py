import unittest
import random

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrSpeed(unittest.TestCase):

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
        self.old = self.fc.speed
        self.speed_values_read = speed_values_read
        self.speed_values_write = speed_values_write

    def test_speed_read(self):
        self.assertIn(self.fc.speed, self.speed_values_read)

    def test_speed_write(self):
        # self.skipTest("needs to be fixed")
        for speed in self.speed_values_write:
            self.fc.speed = speed
            self.assertEqual(speed, self.fc.speed)

    def test_speed_write_invalid(self):
        speed = "asdf"
        with self.assertRaises(CLIError) as e:
            self.fc.speed = speed
        self.assertEqual("The command \" interface " + self.fc.name + " ; switchport speed  " + str(
            speed) + " \" gave the error \" % Invalid command \".", str(e.exception))

    def tearDown(self) -> None:
        if (self.fc.speed != self.old):
            try:
                if ("--" in self.old):
                    self.fc.speed = 'auto'
                else:
                    self.fc.speed = ((int)(self.old)) * 1000  # read in Gbps, write in Mbps
                self.assertEqual(self.old, self.fc.speed)
            except CLIError as e:
                if "port already in a port-channel, no config allowed" in str(e.msg):
                    pass
                else:
                    log.debug("CLIError : " + str(e.msg))
