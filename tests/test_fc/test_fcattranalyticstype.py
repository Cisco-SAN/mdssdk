import unittest

from mdssdk.fc import Fc, InvalidAnalyticsType
from tests.test_fc.fc_vars import *

log = logging.getLogger(__name__)

class TestFcAttrAnalyticsType(unittest.TestCase):

    def setUp(self) -> None:
        self.switch = sw
        log.info(sw.version)
        log.info(sw.ipaddr)
        self.values = analytics_values
        interfaces = sw.interfaces
        while True:
            k,v = random.choice(list(interfaces.items()))
            if (type(v) is Fc):
                self.fc = v
                log.info(k)
                break 
        self.old = self.fc.analytics_type

    def test_analytics_type_read(self):
        self.assertIn(self.fc.analytics_type, self.values)

    def test_analytics_type_write(self):
        for val in self.values:
            self.fc.analytics_type = val
            self.assertEqual(val, self.fc.analytics_type)
        self.fc.analytics_type = self.old
        self.assertEqual(self.old, self.fc.analytics_type)

    def test_analytics_type_write_invalid(self):
        analytics_type = "asdf"
        with self.assertRaises(InvalidAnalyticsType) as e:
            self.fc.analytics_type = analytics_type
        self.assertEqual(
            "InvalidAnalyticsType: Invalid analytics type '" + analytics_type + "'. Valid types are scsi,nvme,all,None(to disable analytics type)",
            str(e.exception))

    def tearDown(self) -> None:
        self.fc.analytics_type = self.old
        self.assertEqual(self.old, self.fc.analytics_type)
