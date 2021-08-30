import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetAddMembers(unittest.TestCase):
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
        self.zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        self.zoneset.create()

    # def test_add_members_nonexisting(self):
    #     zone = Zone(self.switch, "test_zone", self.id)
    #     # TODO: Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
    #     with self.assertRaises(CLIError) as e:
    #         self.zoneset.add_members([zone])
    #     self.assertIn("Zone not present", str(e.exception))

    def test_add_members(self):
        zone1 = Zone(self.switch, "test_zone1", self.id)
        zone1.create()
        zone2 = Zone(self.switch, "test_zone2", self.id)
        zone2.create()
        members = [zone1, zone2]
        self.zoneset.add_members(members)
        self.assertEqual(
            [zone.name for zone in members], list(self.zoneset.members.keys())
        )

    def test_add_members_typeerror(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.add_members("test_zone")
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
