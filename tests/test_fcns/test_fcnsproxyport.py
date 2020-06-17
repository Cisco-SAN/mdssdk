import unittest

from mdssdk.fcns import Fcns
from tests.test_fcns.vars import *

log = logging.getLogger(__name__)


class TestFcnsProxyPort(unittest.TestCase):
    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_proxy_port(self):
        self.skipTest("need to fix")
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]["vsan_id"]
            fcnsentry = fcnsdb[0]["TABLE_fcns_database"]["ROW_fcns_database"]
            if type(fcnsentry) is dict:
                fcnsentry = [fcnsentry]
            pwwn = fcnsentry[0]["pwwn"]
            self.fcns_obj.proxy_port(pwwn=pwwn, vsan=vsan)

    def tearDown(self) -> None:
        pass
