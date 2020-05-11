import unittest

from mdssdk.fc import Fc


class TestFcAttrOutOfService(unittest.TestCase):

    def test_out_of_service_read_error(self):
        fc = Fc(self.switch, self.fc_name[0])
        with self.assertRaises(AttributeError) as e:
            print(fc.out_of_service)
        self.assertEqual("unreadable attribute", str(e.exception))

    def test_out_of_service_write(self):
        fc = Fc(self.switch, self.fc_name[1])
        fc.out_of_service = True
        self.assertEqual('outOfServc', fc.status)
        fc.out_of_service = False
        self.assertIn(fc.status, self.status_values)

    def test_out_of_service_write_invalid(self):
        fc = Fc(self.switch, self.fc_name[2])
        with self.assertRaises(TypeError) as e:
            fc.out_of_service = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))
