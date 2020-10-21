import unittest

from mdssdk.vsan import Vsan
from tests.test_vsan.vars import *

log = logging.getLogger(__name__)


class TestVsanAttrState(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)

    def test_state_read(self):
        self.v.create()
        self.assertIn(self.v.state, ["active", "suspended"])
        self.v.delete()

    def test_state_read_nonexistingvsan(self):
        self.assertIsNone(self.v.state)

    def test_state_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.v.state = "active"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), self.switch.vsans.keys())
