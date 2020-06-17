import unittest
import random

from mdssdk.fcns import Fcns
from tests.test_fcns.vars import *

log = logging.getLogger(__name__)


class TestFcnsStatistics(unittest.TestCase):
    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_statistics(self):
        fcnsdb = self.fcns_obj.statistics()
        if fcnsdb is not None:
            res = self.fcns_obj.statistics(detail=True)
            log.debug(res)
            self.assertIsNotNone(res)

            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]["id"]

            res = self.fcns_obj.statistics(vsan=vsan)
            log.debug(res)
            self.assertIsNotNone(res)

            res = self.fcns_obj.statistics(vsan=vsan, detail=True)
            log.debug(res)
            self.assertIsNotNone(res)

    def test_statistics_nonexistingentry(self):
        fcnsdb = self.fcns_obj.statistics()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan_list = [f["id"] for f in fcnsdb]
            while True:
                vsan = random.randint(2, 400)
                if vsan not in vsan_list:
                    break
            self.assertIsNone(self.fcns_obj.statistics(vsan=vsan))

    def tearDown(self) -> None:
        pass
