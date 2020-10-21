import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneCreate(unittest.TestCase):
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

    def test_create_nonexistingvsan(self):
        self.v.delete()
        self.assertIsNone(self.v.id)
        z = Zone(self.switch, "test_zone", self.id)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertIn("VSAN " + str(self.id) + " is not configured", str(e.exception))

    def test_create(self):
        z = Zone(self.switch, "test_zone", self.id)
        z.create()
        self.assertEqual("test_zone", z.name)

    def test_create_name_invalid(self):
        name = "zone1*!"
        z = Zone(self.switch, name, self.id)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual(
            'The command " zone name '
            + str(name)
            + " vsan "
            + str(self.id)
            + ' " gave the error " Illegal character present in the name ".',
            str(e.exception),
        )

    def test_create_name_invalidfirstchar(self):
        name = "1zone"
        z = Zone(self.switch, name, self.id)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual(
            'The command " zone name '
            + str(name)
            + " vsan "
            + str(self.id)
            + ' " gave the error " Illegal first character (name must start with a letter) ".',
            str(e.exception),
        )

    def test_create_name_beyondmax(self):
        name = "zo123456789123456789123456789123456789123456789123456789123456789"
        z = Zone(self.switch, name, self.id)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual(
            'The command " zone name '
            + str(name)
            + " vsan "
            + str(self.id)
            + ' " gave the error " % String exceeded max length of (64) ".',
            str(e.exception),
        )

    def test_create_name_max(self):
        name = "z123456789123456789123456789123456789123456789123456789123456789"
        z = Zone(self.switch, name, self.id)
        z.create()
        self.assertEqual(name, z.name)

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
