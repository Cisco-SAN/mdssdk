import unittest

from mdssdk.switch import UnsupportedFeature, UnsupportedConfig
from tests.test_switch.switch_vars import *

log = logging.getLogger(__name__)


class TestSwitchFeature(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.name = 'analytics'
        log.debug("Feature " + self.name)
        self.old = self.switch.feature(self.name)

    def test_feature(self):
        self.skipTest("Needs to be fixed")
        old = self.switch.feature(self.name)
        self.switch.feature(self.name, True)
        self.assertTrue(self.switch.feature(self.name))
        self.switch.feature(self.name, False)
        self.assertFalse(self.switch.feature(self.name))
        self.switch.feature(self.name, old)

    def test_feature_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.switch.feature(self.name, "asdf")
        self.assertEqual("enable flag must be True(to enable the feature) or False(to disable the feature)",
                         str(e.exception))

    def test_feature_invalid(self):
        name = "abc"
        with self.assertRaises(UnsupportedFeature) as e:
            self.switch.feature(name, True)
        self.assertEqual("UnsupportedFeature: This feature '" + name + "' is not supported on this switch",
                         str(e.exception))
        with self.assertRaises(UnsupportedFeature) as e:
            self.switch.feature(name, False)
        self.assertEqual("UnsupportedFeature: This feature '" + name + "' is not supported on this switch",
                         str(e.exception))

    def test_feature_notallowed(self):
        for name in ["ssh", "nxapi"]:
            with self.assertRaises(UnsupportedConfig) as e:
                self.switch.feature(name, False)
            self.assertEqual(
                "UnsupportedConfig: Disabling the feature '" + name + "' via this SDK API is not allowed!!",
                str(e.exception))

    def tearDown(self) -> None:
        self.switch.feature(self.name, self.old)
        self.assertEqual(self.old, self.switch.feature(self.name))
