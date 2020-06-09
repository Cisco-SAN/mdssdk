import unittest
import random

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel, PortChannelNotPresent
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelRemoveMembers(unittest.TestCase):

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
        while True:
            k, v = random.choice(list(self.interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.debug(k)
                break

    def test_remove_members_paramtype(self):
        self.pc.create()
        self.pc.add_members([self.fc])
        with self.assertRaises(TypeError) as e:
            self.pc.remove_members(self.fc)
        self.assertEqual("'Fc' object is not iterable", str(e.exception))
        self.pc.delete()

    def test_remove_members_one(self):
        self.pc.create()
        while True:
            k, v = random.choice(list(self.interfaces.items()))
            if (type(v) is Fc and k != self.fc.name):
                fc2 = v
                log.debug(k)
                break
        self.pc.add_members([self.fc, fc2])
        self.pc.remove_members([self.fc])
        self.assertNotIn(self.fc.name, self.pc.members)
        self.assertIn(fc2.name, self.pc.members)
        self.pc.delete()

    def test_remove_members_multiple(self):
        self.pc.create()
        while True:
            k, v = random.choice(list(self.interfaces.items()))
            if (type(v) is Fc and k != self.fc.name):
                fc2 = v
                log.debug(k)
                break
        try:
            self.pc.add_members([self.fc, fc2])
        except CLIError as c:
            if "port not compatible" in c.message:
                self.skipTest("Skipping test as as port not compatible. Please rerun the test cases")
        self.pc.remove_members([self.fc, fc2])
        self.assertIsNone(self.pc.members)
        self.pc.delete()

    def test_remove_members_nonexistingpc(self):
        with self.assertRaises(PortChannelNotPresent) as e:
            self.pc.add_members([self.fc])
        self.assertEqual("PortChannelNotPresent: Port channel " + str(
            self.pc_id) + " is not present on the switch, please create the PC first", str(e.exception))

    def test_remove_members_nonexisting(self):
        self.pc.create()
        with self.assertRaises(CLIError) as e:
            self.pc.remove_members([self.fc])
        self.assertEqual("The command \" interface " + str(self.fc.name) + " ; no channel-group " + str(
            self.pc_id) + " \" gave the error \" " + str(self.fc.name) + ": not part of port-channel \".",
                         str(e.exception))
        self.pc.delete()

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
