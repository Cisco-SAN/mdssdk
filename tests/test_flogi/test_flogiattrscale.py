import logging
import unittest

from mdssdk.flogi import Flogi

log = logging.getLogger(__name__)


class TestFlogiAttrScale(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.flogi_obj = Flogi(switch=self.switch)
        self.old = self.flogi_obj.scale

    def test_scale_read(self):
        self.assertIn(self.flogi_obj.scale, [True, False])

    def test_scale_write(self):
        self.flogi_obj.scale = True
        self.assertEqual(True, self.flogi_obj.scale)
        self.flogi_obj.scale = False
        self.assertEqual(False, self.flogi_obj.scale)

    def test_scale_write_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.flogi_obj.scale = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))

    def tearDown(self) -> None:
        if self.flogi_obj.scale != self.old:
            self.flogi_obj.scale = self.old
            self.assertEqual(self.flogi_obj.scale, self.old)
