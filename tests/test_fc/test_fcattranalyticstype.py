import unittest

from mdssdk.fc import Fc, InvalidAnalyticsType


class TestFcAttrAnalyticsType(unittest.TestCase):

    def test_analytics_type_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        print("Analytics Type " + str(fc.analytics_type))

    def test_analytics_type_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        analytics_type = fc.analytics_type
        values = self.values
        for type in values:
            fc.analytics_type = type
            self.assertEqual(type, fc.analytics_type)
        fc.analytics_type = analytics_type

    def test_status_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        analytics_type = "asdf"
        with self.assertRaises(InvalidAnalyticsType) as e:
            fc.analytics_type = analytics_type
        self.assertEqual(
            "InvalidAnalyticsType: Invalid analytics type '" + analytics_type + "'. Valid types are scsi,nvme,all,None(to disable analytics type)",
            str(e.exception))
