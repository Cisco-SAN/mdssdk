import logging
import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fcns import Fcns

log = logging.getLogger(__name__)


class TestFcnsRejectDuplicatePwwn(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)

    def test_reject_duplicate_pwwn(self):
        self.skipTest("needs to be fixed")
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan = fcnsdb[0]["vsan_id"]
            self.fcns_obj.reject_duplicate_pwwn(vsan=vsan)

    def test_reject_duplicate_pwwn_nonexistingentry(self):
        fcnsdb = self.fcns_obj.database()
        if fcnsdb is not None:
            if type(fcnsdb) is dict:
                fcnsdb = [fcnsdb]
            vsan_list = [f["vsan_id"] for f in fcnsdb]
            while True:
                vsan = random.randint(2, 400)
                if vsan not in vsan_list:
                    break
            with self.assertRaises(CLIError) as e:
                self.fcns_obj.reject_duplicate_pwwn(vsan=vsan)
            self.assertEqual(
                'The command " fcns reject-duplicate-pwwn vsan '
                + str(vsan)
                + ' " gave the error " vsan not present ".',
                str(e.exception),
            )

    def tearDown(self) -> None:
        pass
