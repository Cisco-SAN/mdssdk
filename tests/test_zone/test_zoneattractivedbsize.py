import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.zoneset import ZoneSet
from tests.test_zone.zone_vars import *

log = logging.getLogger(__name__)

class TestZoneAttrActivedbSize(unittest.TestCase):

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
        self.z = Zone(self.switch, self.id, "test_zone")

    def test_activedb_size_read(self):
        self.z.create()
        zoneset = ZoneSet(self.switch, self.id, "test_zoneset")
        zoneset.create()   
        self.z.add_members([{'fcid': '0x123456'}])
        zoneset.add_members([self.z])
        zoneset.activate(True)
        if(zoneset.is_active()):
            self.assertIsNotNone(self.z.activedb_size)
        else:
            self.assertIsNone(self.z.activedb_size)

    def test_activedb_size_read_nonexisting(self):
        self.assertIsNone(self.z.activedb_size)

    def test_activedb_size_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.activedb_size = "asdf"
        self.assertEqual('can\'t set attribute',str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()