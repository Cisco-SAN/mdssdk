import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrModel(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)

    def test_model_read(self):
        model = self.switch.model
        log.debug("Model : " + str(model))
        self.assertRegex(model, "^MDS.*Chassis")

    def test_model_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.model = "mds"
        self.assertEqual("can't set attribute", str(e.exception))

    def tearDown(self) -> None:
        pass
