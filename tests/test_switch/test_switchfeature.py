import unittest

from mdssdk.switch import UnsupportedFeature, UnsupportedConfig
from tests.test_switch.vars import *

log = logging.getLogger(__name__)


class TestSwitchFeature(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.name = "ldap"
        log.debug("Feature " + self.name)
        self.old = self.switch.feature(self.name)

    def test_feature(self):
        old = self.switch.feature(self.name)
        self.switch.feature(self.name, True)
        self.assertTrue(self.switch.feature(self.name))
        self.switch.feature(self.name, False)
        self.assertFalse(self.switch.feature(self.name))
        self.switch.feature(self.name, old)

    def test_feature_typeerror(self):
        with self.assertRaises(TypeError) as e:
            self.switch.feature(self.name, "asdf")
        self.assertIn(
            "enable flag must be True(to enable the feature) or False(to disable the feature)",
            str(e.exception),
        )

    def test_feature_invalid(self):
        name = "abc"
        with self.assertRaises(UnsupportedFeature) as e:
            self.switch.feature(name, True)
        self.assertEqual(
            "UnsupportedFeature: This feature '"
            + name
            + "' is not supported on this switch",
            str(e.exception),
        )
        with self.assertRaises(UnsupportedFeature) as e:
            self.switch.feature(name, False)
        self.assertEqual(
            "UnsupportedFeature: This feature '"
            + name
            + "' is not supported on this switch",
            str(e.exception),
        )

    def test_feature_notallowed(self):
        for name in ["ssh", "nxapi"]:
            with self.assertRaises(UnsupportedConfig) as e:
                self.switch.feature(name, False)
            self.assertEqual(
                "UnsupportedConfig: Disabling the feature '"
                + name
                + "' via this SDK API is not allowed!!",
                str(e.exception),
            )

    def tearDown(self) -> None:
        self.switch.feature(self.name, self.old)
        self.assertEqual(self.old, self.switch.feature(self.name))
