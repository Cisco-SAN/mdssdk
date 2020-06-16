import unittest

from mdssdk.flogi import Flogi
from mdssdk.connection_manager.errors import CLIError
from tests.test_flogi.vars import *

log = logging.getLogger(__name__)

class TestFlogiAttrQuiesce(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.flogi_obj = Flogi(switch=self.switch)
        self.old = self.flogi_obj.quiesce

    def test_quiesce_read(self):
        self.assertIn(self.flogi_obj.quiesce, range(0, 20000))

    def test_quiesce_write(self):
        self.flogi_obj.quiesce = 10
        self.assertEqual(10, self.flogi_obj.quiesce)

    def test_quiesce_write_invalid(self):
        with self.assertRaises(CLIError) as e:
            self.flogi_obj.quiesce = 20001
        self.assertEqual('The command " flogi quiesce timeout 20001 " gave the error " % Invalid number, range is (0:20000) ".', str(e.exception))

    def tearDown(self) -> None:
        if(self.flogi_obj.quiesce != self.old):
            self.flogi_obj.quiesce = self.old
            self.assertEqual(self.flogi_obj.quiesce, self.old)
