import logging
import random
import unittest

from mdssdk.flogi import Flogi

log = logging.getLogger(__name__)


class TestFlogiDatabase(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.flogi_obj = Flogi(switch=self.switch)

    def test_database(self):
        flogidb = self.flogi_obj.database()
        log.debug(flogidb)

        if flogidb is not {}:
            if type(flogidb) is dict:
                flogidb = [flogidb]
            flogidb = self.flogi_obj.database(vsan=flogidb[0]["vsan"])
            log.debug(flogidb)
            self.assertNotEqual({}, flogidb)

            flogidb = self.flogi_obj.database(interface=flogidb[0]["interface"])
            log.debug(flogidb)
            self.assertNotEqual({}, flogidb)

            flogidb = self.flogi_obj.database(fcid=flogidb[0]["fcid"])
            log.debug(flogidb)
            self.assertNotEqual({}, flogidb)
        self.skipTest("need to fix assertion")

    def test_database_nonexistingentry(self):
        flogidb = self.flogi_obj.database()
        if flogidb is not None:
            vsan_list = [f["vsan"] for f in flogidb]

            while True:
                vsan = random.randint(2, 400)
                if vsan not in vsan_list:
                    break
            self.assertEqual({}, self.flogi_obj.database(vsan=vsan))

    def tearDown(self) -> None:
        pass
