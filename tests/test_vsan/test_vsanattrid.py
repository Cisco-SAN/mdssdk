import unittest

from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError
from tests.test_vsan.vsan_vars import *

log = logging.getLogger(__name__)

class TestVsanAttrId(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        self.vsandb = sw.vsans
        while True:
            self.id = get_random_id()
            if str(self.id) not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)         

    def test_id_read(self):
        if self.vsandb:
            self.assertEqual(str(list(self.vsandb.keys())[0]), str(list(self.vsandb.values())[0].id))
        else:
            self.v.create()           
            self.assertEqual(self.id, self.v.id)
            self.v.delete()

    def test_id_read_nonexistingvsan(self):
        self.assertIsNone(self.v.id)

    def test_id_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.v.id = 4
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        if self.v.id is not None:
            v.delete()
        self.assertEqual(self.vsandb.keys(), sw.vsans.keys())
