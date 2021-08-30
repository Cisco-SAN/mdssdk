import random
import unittest

from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrName(unittest.TestCase):
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

    def test_name_read(self):
        self.pc.create()
        self.assertEqual("port-channel" + str(self.pc_id), self.pc.name)
        self.pc.delete()

    def test_name_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.pc.name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
