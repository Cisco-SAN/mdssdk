import unittest

from mdssdk.constants import BASIC, ENHANCED
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone, InvalidZoneMode
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrMode(unittest.TestCase):
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
        self.v.create()
        self.z = Zone(self.switch, "test_zone", self.id)
        self.old = self.z.mode

    def test_mode_read(self):
        self.assertIn(self.z.mode, [BASIC, ENHANCED])

    def test_mode_write(self):
        self.z.create()
        self.z.mode = BASIC
        self.assertEqual(BASIC, self.z.mode)
        self.z.mode = ENHANCED
        self.assertEqual(ENHANCED, self.z.mode)

    def test_mode_write_invalid(self):
        mode = "asdf"
        with self.assertRaises(InvalidZoneMode) as e:
            self.z.mode = mode
        self.assertEqual(
            "InvalidZoneMode: Invalid zone mode "
            + str(mode)
            + " . Valid values are: basic,enhanced",
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.z.mode = self.old
        self.v.delete()
