import unittest

from mdssdk.portchannel import PortChannel
from tests.test_port_channel.vars import *

log = logging.getLogger(__name__)


class TestPortChannelAttrId(unittest.TestCase):

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

    def test_id_read(self):
        self.assertEqual(self.pc_id, self.pc.id)

    def test_id_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.pc.id = 2
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.pc.delete()
        self.assertEqual(self.interfaces.keys(), self.switch.interfaces.keys())
