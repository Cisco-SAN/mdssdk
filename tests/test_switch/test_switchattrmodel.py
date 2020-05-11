import unittest


class TestSwitchAttrModel(unittest.TestCase):
    # model - ro
    def test_model_read(self):
        print("Model : " + str(self.switch.model))

    def test_model_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.model = 'mds'
        self.assertEqual("can't set attribute", str(e.exception))
