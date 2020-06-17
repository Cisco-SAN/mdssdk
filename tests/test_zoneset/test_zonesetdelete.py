import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from mdssdk.zoneset import ZoneSet
from tests.test_zoneset.vars import *

log = logging.getLogger(__name__)


class TestZoneSetDelete(unittest.TestCase):
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
        self.zoneset = ZoneSet(self.switch, "test_zoneset", self.id)

    def test_delete(self):
        self.zoneset.create()
        self.assertEqual("test_zoneset", self.zoneset.name)
        self.zoneset.delete()
        with self.assertRaises(CLIError) as e:
            self.zoneset.name
        self.assertIn("Zoneset not present", str(e.exception))

    def test_delete_nonexisting(self):
        with self.assertRaises(CLIError) as e:
            self.zoneset.delete()
        self.assertIn("Zoneset not present", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
