import unittest

from mdssdk.vsan import Vsan
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetAttrVsan(unittest.TestCase):
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

    def test_vsan_read(self):
        self.assertEqual(self.id, self.zoneset.vsan.id)

    def test_vsan_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.vsan = 5
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
