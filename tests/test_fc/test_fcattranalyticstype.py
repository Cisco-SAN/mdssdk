import random
import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.connection_manager.errors import UnsupportedFeature
from mdssdk.fc import Fc, InvalidAnalyticsType
from tests.test_fc.vars import *

log = logging.getLogger(__name__)


class TestFcAttrAnalyticsType(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.ana_before = self.switch.feature("analytics")
        if not self.ana_before:
            try:
                self.switch.feature("analytics", True)
            except UnsupportedFeature as e:
                self.skipTest(e.message)

        self.anaenabled = self.switch.feature("analytics")
        if not self.anaenabled:
            self.skipTest("Ana feature not enabled or supported")
        self.values = analytics_values
        interfaces = self.switch.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if type(v) is Fc:
                self.fc = v
                mod, port = get_mod_port(self.fc.name)
                modobj = self.switch.modules[mod]
                if modobj.model not in ANA_SUPP_MOD:
                    continue
                log.debug(k)
                break
        self.old = self.fc.analytics_type

    def test_analytics_type_read(self):
        if not self.anaenabled:
            self.skipTest("Analytics feature is not enabled.")
        self.assertIn(self.fc.analytics_type, self.values)

    def test_analytics_type_write(self):
        if not self.anaenabled:
            self.skipTest("Analytics feature is not enabled.")
        try:
            for val in self.values:
                try:
                    self.fc.analytics_type = None
                except CLIError as e:
                    if "Unsupported Port mode of interface" in str(e.message):
                        self.skipTest("Skipping test, port mode is unsupported")
                self.assertEqual(None, self.fc.analytics_type, "port is: " + self.fc.name)
                try:
                    self.fc.analytics_type = val
                except CLIError as e:
                    if "Unsupported Port mode of interface" in str(e.message):
                        self.skipTest("Skipping test, port mode is unsupported")
                self.assertEqual(
                    val, self.fc.analytics_type, "port is: " + self.fc.name
                )
            self.fc.analytics_type = self.old
            self.assertEqual(self.old, self.fc.analytics_type)
        except CLIError as c:
            pass

    def test_analytics_type_write_invalid(self):
        if not self.anaenabled:
            self.skipTest("Analytics feature is not enabled.")
        analytics_type = "asdf"
        with self.assertRaises(InvalidAnalyticsType) as e:
            self.fc.analytics_type = analytics_type
        self.assertEqual(
            "InvalidAnalyticsType: Invalid analytics type:('"
            + analytics_type
            + ")'. Valid types are scsi,nvme,all,None(to disable any analytics type)",
            str(e.exception),
        )

    def tearDown(self) -> None:
        try:
            self.fc.analytics_type = self.old
            self.assertEqual(self.old, self.fc.analytics_type)
            self.switch.feature("analytics", self.ana_before)
            self.assertEqual(self.ana_before, self.switch.feature("analytics"))
        except CLIError as c:
            pass
