import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrFormFactor(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_form_factor_read(self):
        ff = self.switch.form_factor
        log.debug("Form Factor : " + str(ff))
        self.assertRegex(ff, "^9.*")

    def test_form_factor_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.form_factor = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
