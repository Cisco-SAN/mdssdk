import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetAttrActiveMembers(unittest.TestCase):
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
        self.z = ZoneSet(self.switch, "test_zoneset", self.id)
        self.z.create()

    def test_active_members_read(self):
        self.skipTest("not a correct test case Needs to be fixed")
        zone = Zone(self.switch, "test_zone", self.id)
        zone.create()
        zone.add_members([{"fcid": "0x123456"}])
        members = [zone]
        self.z.add_members(members)
        self.z.activate(True)
        if self.z.is_active():
            self.assertEqual(
                [m.name for m in members], list(self.z.active_members.keys())
            )

    def test_active_members_read_nonexisting(self):
        self.skipTest("not a correct test case Needs to be fixed")
        # with self.assertRaises(CLIError) as e:
        #     self.z.active_members
        # self.assertIn("Zoneset not present", str(e.exception))

    def test_active_members_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.active_members = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
