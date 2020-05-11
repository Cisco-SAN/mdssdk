import unittest


class TestSwitchAttrAnalytics(unittest.TestCase):

    def test_analytics_read(self):
        print("Analytics : " + str(self.switch.analytics))

    def test_analytics_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.analytics = "mds"
        self.assertEqual("can't set attribute", str(e.exception))
