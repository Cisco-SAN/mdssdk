import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from tests.test_zoneset.zoneset_vars import *

log = logging.getLogger(__name__)

class TestZoneSetCreate(unittest.TestCase):

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

    def test_create_nonexistingvsan(self):
        self.v.delete()
        self.assertIsNone(self.v.id)
        z = ZoneSet(self.switch, self.id, "test_zoneset")
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertIn("VSAN " + str(self.id) + " is not configured", str(e.exception))

    def test_create(self):
        z = ZoneSet(self.switch, self.id, "test_zoneset")
        z.create()
        self.assertEqual("test_zoneset", z.name)

    def test_create_name_invalid(self):
        invalid = "zoneset1*!"
        z = ZoneSet(self.switch, self.id, invalid)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zoneset name " + str(invalid) + " vsan " + str(
            self.id) + " \" gave the error \" Illegal character present in the name \".", str(e.exception))

    def test_create_name_invalidfirstchar(self):
        invalid = "1zoneset"
        z = ZoneSet(self.switch, self.id, invalid)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zoneset name " + str(invalid) + " vsan " + str(
            self.id) + " \" gave the error \" Illegal first character (name must start with a letter) \".", str(e.exception))

    def test_create_name_beyondmax(self):
        name = 'zo123456789123456789123456789123456789123456789123456789123456789'
        z = ZoneSet(self.switch, self.id, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zoneset name " + name + " vsan " + str(
            self.id) + " \" gave the error \" % String exceeded max length of (64) \".", str(e.exception))

    def test_create_name_max(self):
        name = 'z123456789123456789123456789123456789123456789123456789123456789'
        z = ZoneSet(self.switch, self.id, name)
        z.create()
        self.assertEqual(name, z.name)

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()