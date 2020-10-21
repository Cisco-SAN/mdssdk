import unittest

from mdssdk.constants import PERMIT, DENY
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone, InvalidDefaultZone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrDefaultZone(unittest.TestCase):
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
        self.old = self.z.default_zone

    def test_default_zone_read(self):
        self.assertIn(self.z.default_zone, [PERMIT, DENY])

    def test_default_zone_write(self):
        self.z.default_zone = DENY
        self.assertEqual(DENY, self.z.default_zone)
        self.z.default_zone = PERMIT
        self.assertEqual(PERMIT, self.z.default_zone)

    def test_default_zone_write_invalid(self):
        self.z.create()
        default_zone = "asdf"
        with self.assertRaises(InvalidDefaultZone) as e:
            self.z.default_zone = default_zone
        self.assertIn(
            "Invalid default-zone value "
            + default_zone
            + " . Valid values are: "
            + PERMIT
            + ","
            + DENY,
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.z.default_zone = self.old
        self.v.delete()
