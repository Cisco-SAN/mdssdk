import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetRemoveMembers(unittest.TestCase):
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
        self.zone = Zone(self.switch, "test_zone", self.id)
        self.zone.create()
        self.zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        self.zoneset.create()

    def test_remove_members_nonexisting(self):
        self.assertEqual({}, self.zoneset.members)
        with self.assertRaises(CLIError) as e:
            self.zoneset.remove_members([self.zone])
        self.assertEqual(
            'The command " zoneset name test_zoneset vsan '
            + str(self.id)
            + ' ; no member test_zone " gave the error " Zone not present ".',
            str(e.exception),
        )

    def test_remove_members(self):
        zone1 = self.zone
        zone2 = Zone(self.switch, "test_zone2", self.id)
        zone2.create()
        self.zoneset.add_members([zone1, zone2])
        self.assertIsNotNone(self.zoneset.members)
        self.zoneset.remove_members([zone1, zone2])
        self.assertEqual({}, self.zoneset.members)

    def tearDown(self) -> None:
        self.v.delete()
