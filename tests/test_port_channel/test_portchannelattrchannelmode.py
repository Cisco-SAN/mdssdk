import random
import unittest

from mdssdk.portchannel import PortChannel, PortChannelNotPresent, InvalidChannelMode
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrChannelMode(unittest.TestCase):
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
        if self.switch.npv:
            self.channel_mode_values = channel_mode_values_npv
        else:
            self.channel_mode_values = channel_mode_values

    def test_channel_mode_read_nonexisting(self):
        self.assertIsNone(self.pc.channel_mode)

    def test_channel_mode_read(self):
        self.pc.create()
        self.assertIn(self.pc.channel_mode, self.channel_mode_values)
        self.pc.delete()

    def test_channel_mode_write_nonexisting(self):
        with self.assertRaises(PortChannelNotPresent) as e:
            self.pc.channel_mode = self.channel_mode_values[0]
        self.assertEqual(
            "PortChannelNotPresent: Port channel "
            + str(self.pc_id)
            + " is not present on the switch, please create the PC first",
            str(e.exception),
        )

    def test_channel_mode_write(self):
        self.pc.create()
        for mode in self.channel_mode_values:
            self.pc.channel_mode = mode
            self.assertEqual(mode, self.pc.channel_mode)
        self.pc.delete()

    def test_channel_mode_write_invalid(self):
        channel_mode = "asdf"
        self.pc.create()
        with self.assertRaises(InvalidChannelMode) as e:
            self.pc.channel_mode = channel_mode
        self.assertEqual(
            "InvalidChannelMode: Invalid channel mode ("
            + str(channel_mode)
            + "), Valid values are: on,active",
            str(e.exception),
        )
        self.pc.delete()

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
