import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrMode(unittest.TestCase):
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
        self.mode_values = mode_values

    def test_mode_read(self):
        self.pc.create()
        self.assertIn(self.pc.mode, self.mode_values + ["--"])
        self.pc.delete()

    def test_mode_read_nonexisting(self):
        self.assertIsNone(self.pc.mode)

    def test_mode_write(self):
        self.skipTest("Needs to be fixed")
        self.pc.create()
        oldmode = self.pc.mode
        for mode in self.mode_values:
            self.pc.mode = mode
            self.assertEqual(mode, self.pc.mode)
        if "--" in oldmode:
            oldmode = "auto"
        self.pc.mode = oldmode
        self.pc.delete()

    def test_mode_write_invalid(self):
        mode = "asdf"
        with self.assertRaises(CLIError) as e:
            self.pc.mode = mode
        self.assertEqual(
            'The command " interface port-channel'
            + str(self.pc_id)
            + " ; switchport mode  "
            + str(mode)
            + ' " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
