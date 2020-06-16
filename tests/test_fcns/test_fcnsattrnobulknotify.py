import unittest

from mdssdk.fcns import Fcns
from tests.test_fcns.vars import *

log = logging.getLogger(__name__)

class TestFcnsAttrNoBulkNotify(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.fcns_obj = Fcns(switch=self.switch)
        self.old = self.fcns_obj.no_bulk_notify
    
    def test_no_bulk_notify_read(self):
        self.assertIn(self.fcns_obj.no_bulk_notify, [True, False])

    def test_no_bulk_notify_write(self):
        self.fcns_obj.no_bulk_notify = True
        self.assertEqual(True, self.fcns_obj.no_bulk_notify)
        self.fcns_obj.no_bulk_notify = False
        self.assertEqual(False, self.fcns_obj.no_bulk_notify)

    def test_no_bulk_notify_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.fcns_obj.no_bulk_notify = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))

    def tearDown(self) -> None:
        if(self.fcns_obj.no_bulk_notify != self.old):
            self.fcns_obj.no_bulk_notify = self.old
            self.assertEqual(self.old, self.fcns_obj.no_bulk_notify)
