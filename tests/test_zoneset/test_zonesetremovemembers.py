import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from tests.test_zoneset.zoneset_vars import *

log = logging.getLogger(__name__)

class TestZoneSetRemoveMembers(unittest.TestCase):

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
        self.zone = Zone(self.switch, self.id, "test_zone")
        self.zone.create()
        self.zoneset = ZoneSet(self.switch, self.id, "test_zoneset")
        self.zoneset.create()

    def test_remove_members_nonexisting(self):
        self.assertIsNone(self.zoneset.members)
        with self.assertRaises(CLIError) as e:
            self.zoneset.remove_members([self.zone])
        self.assertEqual('The command " zoneset name test_zoneset vsan ' + str(self.id) + ' ; no member test_zone " gave the error " Zone not present ".', str(e.exception))

    def test_remove_members(self):
        self.skipTest("needs to be fixed")
        zone1 = self.zone
        zone2 = Zone(self.switch, self.id, "test_zone2")
        zone2.create()
        self.zoneset.add_members([zone1, zone2])
        self.assertIsNotNone(self.zoneset.members)
        self.zoneset.remove_members([zone1, zone2])
        self.assertIsNone(self.zoneset.members)

    def tearDown(self) -> None:
        self.v.delete()