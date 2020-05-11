import unittest


class TestSwitchAttrKickstartImage(unittest.TestCase):
    # kickstart_image
    def test_kickstart_image_read(self):
        print("Kickstart Image : " + str(self.switch.kickstart_image))

    def test_kickstart_image_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.kickstart_image = 'asdf'
        self.assertEqual("can't set attribute", str(e.exception))
