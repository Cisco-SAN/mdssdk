import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrActivedbZonesetName(unittest.TestCase):
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
        self.z = Zone(self.switch, "test_zone", self.id)

    def test_activedb_zoneset_name_read(self):
        self.z.create()
        zoneset = ZoneSet(self.switch, "test_zoneset", self.id)
        zoneset.create()
        self.z.add_members([{"fcid": "0x123456"}])
        zoneset.add_members([self.z])
        zoneset.activate(True)
        if zoneset.is_active():
            self.assertEqual("test_zoneset", self.z.activedb_zoneset_name)
        else:
            self.assertIsNone(self.z.activedb_zoneset_name)

    def test_activedb_zoneset_name_read_nonexisting(self):
        self.assertIsNone(self.z.activedb_zoneset_name)

    def test_activedb_zoneset_name_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.activedb_zoneset_name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
