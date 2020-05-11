import unittest


class TestSwitchAttrNpv(unittest.TestCase):
    # npv - ro
    def test_npv_read(self):
        print("Npv switch : " + str(self.switch.npv))

    def test_npv_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.npv = True
        self.assertEqual("can't set attribute", str(e.exception))
