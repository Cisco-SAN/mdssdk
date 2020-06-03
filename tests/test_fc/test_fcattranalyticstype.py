import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.fc import Fc, InvalidAnalyticsType
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrAnalyticsType(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.debug(sw.version)
        log.debug(sw.ipaddr)
        self.values = analytics_values
        interfaces = sw.interfaces
        while True:
            k, v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.debug(k)
                break
        self.old = self.fc.analytics_type

    def test_analytics_type_read(self):
        self.assertIn(self.fc.analytics_type, self.values)

    def test_analytics_type_write(self):
        try:
            for val in self.values:
                try:
                    self.fc.analytics_type = val
                except CLIError as e:
                    if "Unsupported Port mode of interface" in str(e.exception):
                        self.skipTest("Skipping test, port mode is unsupported")
                self.assertEqual(val, self.fc.analytics_type)
            self.fc.analytics_type = self.old
            self.assertEqual(self.old, self.fc.analytics_type)
        except CLIError as c:
            pass

    def test_analytics_type_write_invalid(self):
        analytics_type = "asdf"
        with self.assertRaises(InvalidAnalyticsType) as e:
            self.fc.analytics_type = analytics_type
        self.assertEqual(
            "InvalidAnalyticsType: Invalid analytics type '" + analytics_type + "'. Valid types are scsi,nvme,all,None(to disable analytics type)",
            str(e.exception))

    def tearDown(self) -> None:
        try:
            self.fc.analytics_type = self.old
            self.assertEqual(self.old, self.fc.analytics_type)
        except CLIError as c:
            pass
