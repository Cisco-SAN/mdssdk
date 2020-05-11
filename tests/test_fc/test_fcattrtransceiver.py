import unittest

from mdssdk.fc import Fc


class TestFcAttrTransceiver(unittest.TestCase):

    def test_transceiver_read(self):
        interfaces = self.switch.interfaces
        sfp_present, sfp_absent = 0, 0
        for key in interfaces:
            if (type(interfaces[key]) is not Fc):
                continue
            fc = Fc(self.switch, key)
            temp = [x for x in dir(fc.transceiver) if not x.startswith('_')]
            self.assertIn(fc.transceiver.sfp_present, [True, False])
            if (fc.transceiver.sfp_present and sfp_present == 0):
                print(str(key) + " transceiver : ")
                for t in temp:
                    print(str(t) + " : " + str(fc.transceiver.__getattribute__(t)))
                sfp_present = 1
            elif ((not fc.transceiver.sfp_present) and sfp_absent == 0):
                print("\n" + str(key) + " transceiver : ")
                for t in temp:
                    print(str(t) + " : " + str(fc.transceiver.__getattribute__(t)))
                sfp_absent = 1
            if sfp_present == 1 and sfp_absent == 1:
                break

    def test_transceiver_write_error(self):
        fc = Fc(self.switch, "fc1/1")
        with self.assertRaises(AttributeError) as e:
            fc.transceiver = []
        self.assertEqual("can't set attribute", str(e.exception))
