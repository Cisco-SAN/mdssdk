import unittest
import random

from mdssdk.portchannel import PortChannel, InvalidPortChannelRange
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelCreate(unittest.TestCase):
    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.interfaces = sw.interfaces
        while True:
            self.pc_id = random.randint(1, 256)
            if "port-channel" + str(self.pc_id) not in self.interfaces.keys():
                break
        self.pc = PortChannel(self.switch, self.pc_id)

    def test_create(self):
        self.pc.create()
        self.assertIsNotNone(self.pc.channel_mode)
        self.pc.delete()

    def test_create_invalid(self):
        for i in [0, 257]:
            with self.assertRaises(InvalidPortChannelRange) as e:
                pc = PortChannel(self.switch, i)
            self.assertEqual(
                "InvalidPortChannelRange: Port channel id "
                + str(i)
                + " is invalid, id should range from 1 to 256",
                str(e.exception),
            )

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
