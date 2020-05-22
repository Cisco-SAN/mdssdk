import unittest

from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from tests.test_vsan.vsan_vars import *

log = logging.getLogger(__name__)

class TestVsanCreate(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        self.vsandb = sw.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id) 
        self.boundary_id = boundary_id
        self.reserved_id = reserved_id

    def test_create_success(self):
        self.v.create("test_vsan_create")
        self.assertEqual(self.id, self.v.id)
        self.v.delete()

    def test_create_boundary(self):
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.create()
            self.assertEqual(
                'The command " vsan database ; vsan ' + str(i) + ' " gave the error " % Invalid command ".',
                str(e.exception))

    def test_create_reserved(self):
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.create()
            self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' " gave the error " vsan ' + str(
                i) + ':vsan(s) reserved ".', str(e.exception))

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), sw.vsans.keys())
