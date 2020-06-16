import unittest
import random

from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrMembers(unittest.TestCase):
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

    def test_members_read_nonexisting(self):
        self.assertIsNone(self.pc.members)

    def test_members_read(self):
        self.pc.create()
        while True:
            k, v = random.choice(list(self.interfaces.items()))
            if type(v) is Fc:
                fc = v
                log.debug(k)
                break
        self.pc.add_members([fc])
        self.assertIn(fc.name, self.pc.members)
        self.pc.delete()

    def test_members_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.pc.members = []
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
