import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestZoneSetDelete(unittest.TestCase):

    def test_delete(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = ZoneSet(self.switch, v, self.zoneset_name[0])
        z.create()
        z.delete()
        self.assertIsNone(z.name)
        v.delete()

    def test_delete_nonexisting(self):
        i = self.vsan_id[1]
        v = Vsan(self.switch, i)
        v.create()
        zonesetname = self.zoneset_name[1]
        z = ZoneSet(self.switch, v, zonesetname)
        with self.assertRaises(CLIError) as e:
            z.delete()
        self.assertEqual('The command " no zoneset name ' + str(zonesetname) + ' vsan ' + str(
            i) + ' " gave the error " Zoneset not present ".', str(e.exception))
        v.delete()
