import unittest
import random

from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelDelete(unittest.TestCase):
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

    def test_delete_nonexisting(self):
        self.assertIsNone(self.pc.channel_mode)
        self.pc.delete()  # no error
        self.assertIsNone(self.pc.channel_mode)

    def test_delete(self):
        self.pc.create()
        self.assertIsNotNone(self.pc.channel_mode)
        self.pc.delete()
        self.assertIsNone(self.pc.channel_mode)

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
