import unittest

from mdssdk.fc import Fc


class TestFcAttrName(unittest.TestCase):

    def test_name_read(self):
        fc = Fc(self.switch, self.fc_name[0])
        self.assertEqual(self.fc_name[0], fc.name)

    def test_name_write_error(self):
        fc = Fc(self.switch, self.fc_name[1])
        with self.assertRaises(AttributeError) as e:
            fc.name = "asdf"
        self.assertEqual("can't set attribute", str(e.exception))
