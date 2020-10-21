import unittest

from mdssdk.vsan import Vsan
from tests.test_vsan.vars import *

log = logging.getLogger(__name__)


class TestVsanAttrSuspend(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)

    def test_suspend_write(self):
        self.v.create()
        self.v.suspend = True
        self.assertEqual("suspended", self.v.state)
        self.v.suspend = False
        self.assertEqual("active", self.v.state)
        self.v.delete()

    def test_suspend_read_error(self):
        with self.assertRaises(AttributeError) as e:
            log.debug(self.v.suspend)
        self.assertEqual("unreadable attribute", str(e.exception))

    def test_suspend_write_nonexistingvsan(self):
        self.v.suspend = True  # writing suspend value creates vsan
        self.assertEqual("suspended", self.v.state)
        self.v.delete()

    def test_suspend_write_invalid(self):
        with self.assertRaises(TypeError) as e:
            self.v.suspend = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), self.switch.vsans.keys())
