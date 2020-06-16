import unittest

from mdssdk.fcns import Fcns
from tests.test_fcns.vars import *

log = logging.getLogger(__name__)

class TestFcnsAttrZoneLookupCache(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)
        self.old = self.fcns_obj.zone_lookup_cache

    def test_zone_lookup_cache_read(self):
        self.assertIn(self.fcns_obj.zone_lookup_cache, [True, False])

    def test_zone_lookup_cache_write(self):
        self.fcns_obj.zone_lookup_cache = True
        self.assertEqual(True, self.fcns_obj.zone_lookup_cache)
        self.fcns_obj.zone_lookup_cache = False
        self.assertEqual(False, self.fcns_obj.zone_lookup_cache)

    def test_zone_lookup_cache_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.fcns_obj.zone_lookup_cache = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))
        
    def tearDown(self) -> None:
        if(self.fcns_obj.zone_lookup_cache != self.old):
            self.fcns_obj.zone_lookup_cache = self.old
            self.assertEqual(self.old, self.fcns_obj.zone_lookup_cache)