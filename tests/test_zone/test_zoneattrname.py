import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAttrName(unittest.TestCase):
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
        self.z = Zone(self.switch, "test_zone", self.id)

    def test_name_read(self):
        self.z.create()
        self.assertEqual("test_zone", self.z.name)

    def test_name_read_nonexisting(self):
        # TODO: Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
        # with self.assertRaises(CLIError) as c:
        #     self.z.name
        # self.assertIn("Zone not present", str(c.exception))
        self.assertIsNone(self.z.name)

    def test_name_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.z.name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
