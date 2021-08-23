import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from tests.test_vsan.vars import *

log = logging.getLogger(__name__)


class TestVsanAttrName(unittest.TestCase):
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

    def test_name_read(self):
        name = "test___vsan___name"
        self.v.create(name)
        self.assertEqual(name, self.v.name)
        self.v.delete()

    def test_name_read_nonexistingvsan(self):
        self.assertIsNone(self.v.name)

    def test_name_write(self):
        self.v.create()
        self.v.name = "test__name"
        self.assertEqual("test__name", self.v.name)
        self.v.delete()

    def test_name_write_max32(self):
        self.v.create()
        name = "12345678912345678912345678912345"
        self.v.name = name
        self.assertEqual(name, self.v.name)
        self.v.delete()

    def test_name_write_beyondmax(self):
        self.v.create()
        name = "123456789123456789123456789123456"
        with self.assertRaises(CLIError) as e:
            self.v.name = name
        self.assertIn("String exceeded max length of (32)", str(e.exception))
        self.v.delete()

    def test_name_write_repeated(self):
        name = "test___repeated___name"
        self.v.create(name)
        while True:
            i = get_random_id()
            if i not in self.switch.vsans.keys():
                break
        v1 = Vsan(switch=self.switch, id=i)
        with self.assertRaises(CLIError) as e:
            v1.name = name
        self.assertIn("vsan name is already in use", str(e.exception))
        self.v.delete()

    def test_name_write_nonexistingvsan(self):
        self.v.name = (
            "vsantest"  ## writing name creates vsan on switch if it doesn't exist
        )
        self.assertEqual(self.id, self.v.id)
        self.v.delete()

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), self.switch.vsans.keys())
