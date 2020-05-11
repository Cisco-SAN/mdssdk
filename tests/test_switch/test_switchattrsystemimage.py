import unittest


class TestSwitchAttrSystemImage(unittest.TestCase):
    # system_image
    def test_system_image_read(self):
        print("System Image : " + str(self.switch.system_image))

    def test_system_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.system_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))
