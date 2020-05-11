import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneDelete(unittest.TestCase):

    def test_delete(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        zonename = self.zone_name[0]
        z = Zone(self.switch, v, zonename)
        z.create()
        self.assertEqual(zonename, z.name)
        z.delete()
        self.assertIsNone(z.name)
        v.delete()

    def test_delete_nonexisting(self):
        i = self.vsan_id[1]
        zonename = self.zone_name[1]
        v = Vsan(self.switch, i)
        v.create()
        z = Zone(self.switch, v, zonename)
        with self.assertRaises(CLIError) as e:
            z.delete()
        self.assertEqual('The command " no zone name ' + str(zonename) + ' vsan ' + str(
            i) + ' " gave the error " Zone not present ".', str(e.exception))
        v.delete()
