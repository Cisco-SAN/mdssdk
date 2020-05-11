import unittest

from mdssdk.fc import Fc


class TestFcAttrCounters(unittest.TestCase):

    def test_counters_read(self):
        interfaces = self.switch.interfaces
        for key in interfaces:
            if (type(interfaces[key]) is not Fc):
                continue
            fc = Fc(self.switch, key)
            temp = [x for x in dir(fc.counters) if not x.startswith('_')]
            none_attr = []
            for t in temp:
                if (fc.counters.__getattribute__(t) is None):
                    none_attr.append(t)
            if (key == "fc1/1"):
                print("fc1/1 Counters : ")
                for t in temp:
                    print(str(t) + " : " + str(fc.counters.__getattribute__(t)))
            print("Counter attributes that returned None : " + str(none_attr))

    def test_counters_write_error(self):
        fc = Fc(self.switch, "fc1/1")
        with self.assertRaises(AttributeError) as e:
            fc.counters = "mds"
        self.assertEqual("can't set attribute", str(e.exception))
