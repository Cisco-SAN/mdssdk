import unittest
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanCreate(unittest.TestCase):

    def test_create_success(self):
        i = self.create_id
        v = Vsan(switch=self.switch, id=i)
        if v.id is not None:
            v.delete()
        self.assertIsNone(v.id)
        v.create()
        self.assertEqual(i, v.id)
        v.delete()

    def test_create_boundary(self):
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.create()
            self.assertEqual(
                'The command " vsan database ; vsan ' + str(i) + ' " gave the error " % Invalid command ".',
                str(e.exception))

    def test_create_reserved(self):
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.create()
            self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' " gave the error " vsan ' + str(
                i) + ':vsan(s) reserved ".', str(e.exception))

    def test_create_max_vsans_fail(self):
        v = []
        with self.assertRaises(CLIError) as e:
            for i in self.max_vsan_fail:
                v.append(Vsan(switch=self.switch, id=i))
                v[i - 2].create()
        self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' " gave the error " vsan ' + str(
            i) + ':maximum number of vsans already configured ".', str(e.exception))
        for j in range(2, i):
            v[j - 2].delete()

    def test_create_max_vsans_success(self):
        v = []
        ctr = len(self.switch.vsans)
        for i in self.max_vsan_success:
            if (ctr == 256):
                break
            v.append(Vsan(switch=self.switch, id=i))
            v[i - 2].create()
            self.assertEqual(i, v[i - 2].id)
            ctr += 1
        for i in v:
            i.delete()

    def test_create_samevsan_multipletimes(self):
        v1 = Vsan(switch=self.switch, id=1)
        v1.create("defaultvsan1")
        self.assertEqual("defaultvsan1", v1.name)
        v1.create("VSAN0001")
        for i in range(1, 10):
            v2 = Vsan(switch=self.switch, id=self.create_multiple_id)
            v2.create(str(i))
            self.assertEqual(str(i), v2.name)
        v2.delete()
