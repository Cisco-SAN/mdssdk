import unittest

from mdssdk.vsan import Vsan
from tests.test_vsan.vars import *

log = logging.getLogger(__name__)


class TestVsanAttrInterfaces(unittest.TestCase):
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

    def test_interfaces_read(self):
        ## reading interfaces in default vsan 1
        self.assertIsNotNone(self.vsandb[1].interfaces)

    def test_interfaces_read_nonexistingvsan(self):
        self.assertIsNone(self.v.interfaces)

    def test_interfaces_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.v.interfaces = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), self.switch.vsans.keys())
