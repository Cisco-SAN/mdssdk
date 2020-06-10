import unittest
import random

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel, PortChannelNotPresent
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAddMembers(unittest.TestCase):

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

    def test_add_members_paramtype(self):
        self.pc.create()
        with self.assertRaises(TypeError) as e:
            self.pc.add_members(self.fc)
        self.assertEqual("'Fc' object is not iterable", str(e.exception))
        self.pc.delete()

    def test_add_members_one(self):
        self.pc.create()
        self.pc.add_members([self.fc])
        self.assertIn(self.fc.name, self.pc.members)
        self.pc.delete()

    def test_add_members_multiple(self):
        self.pc.create()
        while True:
            k, v = random.choice(list(self.interfaces.items()))
            if (type(v) is Fc and k != self.fc.name):
                fc2 = v
                log.debug(k)
                break
        self.pc.add_members([self.fc, fc2])
        self.assertIn(self.fc.name, self.pc.members)
        self.assertIn(fc2.name, self.pc.members)
        self.pc.delete()

    def test_add_members_nonexisting(self):
        with self.assertRaises(PortChannelNotPresent) as e:
            self.pc.add_members([self.fc])
        self.assertEqual("PortChannelNotPresent: Port channel " + str(
            self.pc_id) + " is not present on the switch, please create the PC first", str(e.exception))

    def test_add_members_invalidfc(self):
        invalidfc = "fc48/48"  ### check
        fc1 = Fc(self.switch, invalidfc)
        self.pc.create()
        with self.assertRaises(CLIError) as e:
            self.pc.add_members([fc1])
        self.assertEqual("The command \" interface " + str(invalidfc) + " ; channel-group " + str(
            self.pc_id) + " force \" gave the error \" Invalid interface format \".", str(e.exception))
        self.pc.delete()

    def test_add_members_invalid(self):
        self.pc.create()
        with self.assertRaises(AttributeError) as e:
            self.pc.add_members(["fc1/1"])
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))
        self.pc.delete()

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertCountEqual(self.interfaces.keys(), self.switch.interfaces.keys())
