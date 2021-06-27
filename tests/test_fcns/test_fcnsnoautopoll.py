import logging
import unittest

from mdssdk.fcns import Fcns

log = logging.getLogger(__name__)


class TestFcnsNoAutoPoll(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_no_auto_poll(self):
        self.fcns_obj.no_auto_poll()
        self.skipTest("need to fix")
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]["vsan_id"]
            fcnsentry = fcnsdb[0]["TABLE_fcns_database"]["ROW_fcns_database"]  # change
            if type(fcnsentry) is dict:
                fcnsentry = [fcnsentry]
            pwwn = fcnsentry[0]["pwwn"]
            self.fcns_obj.no_auto_poll(vsan=vsan)
            self.fcns_obj.no_auto_poll(pwwn=pwwn)

    def tearDown(self) -> None:
        pass
