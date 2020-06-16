import unittest
import random

from mdssdk.fcns import Fcns
from tests.test_fcns.vars import *

log = logging.getLogger(__name__)

class TestFcnsDatabase(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_database(self):
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            res = self.fcns_obj.database(detail = True)
            log.debug(res)
            self.assertIsNotNone(res)

            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]['vsan_id']
            fcnsentry = fcnsdb[0]['TABLE_fcns_database']['ROW_fcns_database']
            if type(fcnsentry) is dict:
                fcnsentry = [fcnsentry]
            fcid = fcnsentry[0]['fcid']

            res = self.fcns_obj.database(vsan = vsan)
            log.debug(res)
            self.assertIsNotNone(res)

            res = self.fcns_obj.database(vsan = vsan, detail = True)
            log.debug(res)
            self.assertIsNotNone(res)

            res = self.fcns_obj.database(vsan = vsan, fcid = fcid)
            log.debug(res)
            self.assertIsNotNone(res)

            res = self.fcns_obj.database(vsan = vsan, fcid = fcid, detail = True)
            log.debug(res)
            self.assertIsNotNone(res)

    def test_database_nonexistingentry(self):
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan_list = [f['vsan_id'] for f in fcnsdb]

            while True:
                vsan = random.randint(2, 400)
                if vsan not in vsan_list:
                    break
            self.assertIsNone(self.fcns_obj.database(vsan = vsan))      

    def tearDown(self) -> None:
        pass
