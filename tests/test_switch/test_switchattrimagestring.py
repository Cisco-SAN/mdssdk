import unittest


class TestSwitchAttrImageString(unittest.TestCase):
    # image_string - ro
    def test_image_string_read(self):
        print("Image String : " + str(self.switch.image_string))

    def test_image_string_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.image_string = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))
