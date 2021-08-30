import unittest

from mdssdk.vsan import Vsan
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetAttrName(unittest.TestCase):
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

    def test_name_read(self):
        self.zoneset.create()
        self.assertEqual("test_zoneset", self.zoneset.name)

    # def test_name_read_nonexisting(self):
    #     # TODO: Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
    #     with self.assertRaises(CLIError) as c:
    #         self.zoneset.name
    #     self.assertIn("Zoneset not present", str(c.exception))

    def test_name_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.zoneset.name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
