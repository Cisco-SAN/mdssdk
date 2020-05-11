import unittest


class TestSwitchAttrIpAddr(unittest.TestCase):

    def test_ipaddr_read(self):
        self.assertEqual(self.ip_address, self.switch.ipaddr)

    def test_ipaddr_write_error(self):
        with self.assertRaises(AttributeError) as e:
            self.switch.ipaddr = '10.197.155.244'
        self.assertEqual("can't set attribute", str(e.exception))
