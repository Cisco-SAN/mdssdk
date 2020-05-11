import unittest


class TestSwitchAttrVsans(unittest.TestCase):

    def test_vsans_read(self):
        print("Vsans : " + str(self.switch.vsans.keys()))

    def test_vsans_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.vsans = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))
