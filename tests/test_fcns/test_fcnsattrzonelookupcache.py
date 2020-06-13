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

    def test_zone_lookup_cache_write(self):
        self.skipTest("need to fix")
        # didn't get how to assert 
        self.fcns_obj.zone_lookup_cache = True

    def test_zone_lookup_cache_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.fcns_obj.zone_lookup_cache = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))
        
    def tearDown(self) -> None:
        pass
