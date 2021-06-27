import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrSpeed(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.interfaces = self.switch.interfaces
        while True:
            self.pc_id = random.randint(1, 256)
            if "port-channel" + str(self.pc_id) not in self.interfaces.keys():
                break
        self.pc = PortChannel(self.switch, self.pc_id)
        self.speed_values_read = speed_values_read
        self.speed_values_write = speed_values_write

    def test_speed_read(self):
        self.pc.create()
        self.assertIn(self.pc.speed, self.speed_values_read)
        self.pc.delete()

    def test_speed_read_nonexisting(self):
        self.assertIsNone(self.pc.speed)

    def test_speed_write(self):
        self.skipTest("Needs to be fixed")
        self.pc.create()
        oldspeed = self.pc.speed
        for speed in self.speed_values_write:
            self.pc.speed = speed
            self.assertEqual(speed, self.pc.speed)
        if "--" in oldspeed:
            oldspeed = "auto"
        self.pc.speed = oldspeed
        self.pc.delete()

    def test_speed_write_invalid(self):
        speed = "asdf"
        with self.assertRaises(CLIError) as e:
            self.pc.speed = speed
        self.assertEqual(
            'The command " interface port-channel'
            + str(self.pc_id)
            + " ; switchport speed  "
            + str(speed)
            + ' " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
