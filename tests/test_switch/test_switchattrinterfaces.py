import unittest


class TestSwitchAttrInterfaces(unittest.TestCase):
    # interfaces - list
    def test_interfaces_read(self):
        print("Interfaces : " + str(self.switch.interfaces.keys()))

    def test_interfaces_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.interfaces = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))
