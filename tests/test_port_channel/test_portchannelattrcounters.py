import unittest
import random

from mdssdk.connection_manager.errors import CLIError
from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrCounters(unittest.TestCase):
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

    def test_counters_read_nonexisting(self):
        with self.assertRaises(CLIError) as e:
            log.debug(self.pc.counters.__getattribute__("brief"))
        self.assertIn("Invalid range", str(e.exception))
        self.pc.delete()

    def test_counters_read(self):
        self.pc.create()
        self.assertIsNotNone(self.pc.counters, "pc.counters did not get counter objects")
        dir_counters = [x for x in dir(self.pc.counters) if not x.startswith("_")]
        for t in dir_counters:
            val = self.pc.counters.__getattribute__(t)
            log.debug(str(t) + " " + str(val))
            if t is not "other_stats":
                self.assertIsNotNone(val)
            else:
                self.assertIsNone(val)
        self.pc.delete()

    def test_counters_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.pc.counters = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def test_counters_clear(self):
        self.skipTest("Needs to be fixed")
        self.pc.counters.clear()

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
