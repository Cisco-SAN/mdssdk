import unittest


class TestSwitchAttrType(unittest.TestCase):
    # type - ro
    def test_type_read(self):
        print("Type : " + str(self.switch.type))

    def test_type_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.type = "mds"
        self.assertEqual("can't set attribute", str(e.exception))
