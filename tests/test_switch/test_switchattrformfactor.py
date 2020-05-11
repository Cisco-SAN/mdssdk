import unittest


class TestSwitchAttrFormFactor(unittest.TestCase):
    # form factor - ro
    def test_form_factor_read(self):
        print("Form Factor : " + str(self.switch.form_factor))

    def test_form_factor_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.form_factor = "mds"
        self.assertEqual("can't set attribute", str(e.exception))
