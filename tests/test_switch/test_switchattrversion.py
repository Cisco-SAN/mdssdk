import unittest


class TestSwitchAttrVersion(unittest.TestCase):
    # version - ro
    def test_version_read(self):
        print("Version : " + str(self.switch.version))

    def test_version_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.version = '8.4'
        self.assertEqual("can't set attribute", str(e.exception))
