import unittest

from mdssdk.vsan import Vsan
from mdssdk.zone import Zone


class TestZoneAttrEffectivedbSizePercentage(unittest.TestCase):

    def test_effectivedb_size_percentage_read(self):
        v = Vsan(self.switch, self.vsan_id[0])
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        log.debug("Effective DB Size Percentage : " + str(z.effectivedb_size_percentage))
        self.assertIsNotNone(z.effectivedb_size_percentage)
        v.delete()

    def test_effectivedb_size_percentage_read_nonexisting(self):
        v = Vsan(self.switch,self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        log.debug("Effective DB Size Percentage(nonexisting) : " + str(z.effectivedb_size_percentage))
        self.assertIsNotNone(z.effectivedb_size_percentage)
        v.delete()

    def test_effectivedb_size_percentage_write_error(self):
        v = Vsan(self.switch,self.vsan_id[2])
        v.create()
        z = Zone(self.switch, v, self.zone_name[2])
        with self.assertRaises(AttributeError) as e:
            z.effectivedb_size_percentage = "asdf"
        self.assertEqual('can\'t set attribute',str(e.exception))
        v.delete()