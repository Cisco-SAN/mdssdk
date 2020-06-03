import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan
from tests.test_zoneset.zoneset_vars import *

log = logging.getLogger(__name__)

class TestZoneSetAttrVsan(unittest.TestCase):

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
        self.zoneset = ZoneSet(self.switch, self.id, "test_zoneset")

    def test_vsan_read(self):
        self.assertEqual(self.id, self.zoneset.vsan.id)

    def test_vsan_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.vsan = 5
        self.assertEqual('can\'t set attribute', str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()