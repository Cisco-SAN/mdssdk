import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrDescription(unittest.TestCase):
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

    def test_description_read(self):
        self.pc.create()
        self.assertIsNotNone(self.pc.description)
        self.pc.delete()

    def test_description_read_nonexisting(self):
        with self.assertRaises(CLIError) as e:
            log.debug(self.pc.description)
        self.assertIn("Invalid range", str(e.exception))

    def test_description_write_max254(self):
        self.pc.create()
        old = self.pc.description
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch123456789123456789123456"
        self.pc.description = desc
        self.assertEqual(desc, self.pc.description)
        self.pc.description = old
        self.pc.delete()

    def test_description_write_beyondmax(self):
        desc = "switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678switch12345678912345678912345678"
        with self.assertRaises(CLIError) as e:
            self.pc.description = desc
        self.assertIn("String exceeded max length of (254)", str(e.exception))
        self.pc.delete()

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
