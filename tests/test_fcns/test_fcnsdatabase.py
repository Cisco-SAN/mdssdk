import logging
import random
import unittest

from mdssdk.fcns import Fcns

log = logging.getLogger(__name__)


class TestFcnsDatabase(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_database(self):
        fcnsdb = self.fcns_obj.database()
        log.debug(fcnsdb)

        if fcnsdb is not {}:
            res = self.fcns_obj.database(detail=True)
            log.debug(res)
            self.assertNotEqual({}, res)

            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]["vsan_id"]

            res = self.fcns_obj.database(vsan=vsan)
            log.debug(res)
            self.assertNotEqual({}, res)

            res = self.fcns_obj.database(vsan=vsan, detail=True)
            log.debug(res)
            self.assertNotEqual({}, res)
            """fcnsentry = fcnsdb[0]["TABLE_fcns_database"]["ROW_fcns_database"] #change
            if type(fcnsentry) is dict:
                fcnsentry = [fcnsentry]
            fcid = fcnsentry[0]["fcid"]

            res = self.fcns_obj.database(vsan=vsan, fcid=fcid)
            log.debug(res)
            self.assertNotEqual({}, res)

            res = self.fcns_obj.database(vsan=vsan, fcid=fcid, detail=True)
            log.debug(res)
            self.assertNotEqual({}, res)"""
        self.skipTest("need to fix assertion")

    def test_database_nonexistingentry(self):
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan_list = [f["vsan_id"] for f in fcnsdb]

            while True:
                vsan = random.randint(2, 400)
                if vsan not in vsan_list:
                    break
            self.assertEqual({}, self.fcns_obj.database(vsan=vsan))

    def tearDown(self) -> None:
        pass
