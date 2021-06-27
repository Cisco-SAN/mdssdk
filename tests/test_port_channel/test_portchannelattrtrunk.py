import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrTrunk(unittest.TestCase):
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
        self.trunk_values = trunk_values

    def test_trunk_read(self):
        self.pc.create()
        self.assertIn(self.pc.trunk, self.trunk_values)
        self.pc.delete()

    def test_trunk_read_nonexisting(self):
        self.assertIsNone(self.pc.trunk)

    def test_trunk_write(self):
        self.pc.create()
        oldtrunk = self.pc.trunk
        for trunk in self.trunk_values:
            self.pc.trunk = trunk
            self.assertEqual(trunk, self.pc.trunk)
        self.pc.trunk = oldtrunk
        self.pc.delete()

    def test_trunk_write_invalid(self):
        trunk = "asdf"
        with self.assertRaises(CLIError) as e:
            self.pc.trunk = trunk
        self.assertEqual(
            'The command " interface port-channel'
            + str(self.pc_id)
            + " ; switchport trunk mode  "
            + str(trunk)
            + ' " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
