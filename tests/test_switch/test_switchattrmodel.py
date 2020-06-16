import unittest

from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchAttrModel(unittest.TestCase):
    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)

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
