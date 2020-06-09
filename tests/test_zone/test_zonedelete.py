import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneDelete(unittest.TestCase):

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

    def test_delete(self):
        self.z.create()
        self.assertEqual('test_zone', self.z.name)
        self.z.delete()
        self.assertIsNone(self.z.name)

    def test_delete_nonexisting(self):
        with self.assertRaises(CLIError) as e:
            self.z.delete()
        self.assertEqual('The command " no zone name test_zone vsan ' + str(
            self.id) + ' " gave the error " Zone not present ".', str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
