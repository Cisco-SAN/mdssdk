import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet, ZoneNotPresent
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetAddMembers(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.vsandb = sw.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()
        self.zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        self.zoneset.create()

    def test_add_members_nonexisting(self):
        zone = Zone(self.switch, "test_zone", self.id)
        with self.assertRaises(ZoneNotPresent) as e:
            self.zoneset.add_members([zone])
        self.assertEqual("ZoneNotPresent: The given zoneset member 'test_zone' is not present in the switch.",
                         str(e.exception))

    def test_add_members(self):
        self.skipTest("needs to be fixed")
        zone1 = Zone(self.switch, "test_zone1", self.id)
        zone1.create()
        zone2 = Zone(self.switch, "test_zone2", self.id)
        zone2.create()
        members = [zone1, zone2]
        self.zoneset.add_members(members)
        self.assertEqual([zone.name for zone in members], list(self.zoneset.members.keys()))

    def test_add_members_typeerror(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.add_members("test_zone")
        self.assertEqual("'str' object has no attribute 'name'", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
