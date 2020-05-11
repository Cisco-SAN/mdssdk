import unittest
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanAttrName(unittest.TestCase):

    def test_name_read(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[0])
        v.create()
        self.assertEqual("VSAN0002", v.name)
        v.delete()

    def test_name_read_nonexistingvsan(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[1])
        if v.id is not None:
            v.delete()
        self.assertIsNone(v.name)
        id_list = [0, 4095, 4079, 4094]
        for i in id_list:
            v = Vsan(switch=self.switch, id=i)
            self.assertIsNone(v.name)

    def test_name_change(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[2])
        v.create()
        v.name = "test__name"
        self.assertEqual("test__name", v.name)
        v.delete()

    def test_name_write_max32(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[3])
        v.create()
        name = self.max32_name
        v.name = name
        self.assertEqual(name, v.name)
        v.delete()

    def test_name_write_beyondmax(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[4])
        v.create()
        name = self.beyondmax_name
        with self.assertRaises(CLIError) as e:
            v.name = name
        self.assertEqual('The command " vsan database ; vsan ' + str(self.vsan_id[4]) + ' name \'' + str(
            name) + '\' " gave the error " % String exceeded max length of (32) ".', str(e.exception))
        v.delete()

    def test_name_write_specialchar(self):
        i = self.vsan_id[5]
        v = Vsan(switch=self.switch, id=i)
        v.create()
        name = self.specialchar_name
        with self.assertRaises(CLIError) as e:
            v.name = name
        self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' name \'' + str(
            name) + '\' " gave the error " Request contains invalid special characters ".', str(e.exception))
        v.delete()

    def test_name_write_repeated(self):
        i = self.vsan_id[6]
        v = Vsan(switch=self.switch, id=i)
        v.create()
        name = self.repeated_name
        with self.assertRaises(CLIError) as e:
            v.name = name
        self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' name \'' + str(
            name) + '\' " gave the error " vsan ' + str(i) + ':vsan name is already in use ".', str(e.exception))
        v.delete()

    def test_name_write_nonexistingvsan(self):
        i = self.vsan_id[7]
        v = Vsan(switch=self.switch, id=i)
        if v.id is not None:
            v.delete()
        v.name = "vsantest"
        self.assertEqual(i, v.id)
        v.delete()

    def test_name_write_boundary(self):
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.name = 'vsan'
            self.assertEqual('The command " vsan database ; vsan ' + str(
                i) + ' name \'vsan\' " gave the error " % Invalid command ".', str(e.exception))

    def test_name_write_reserved(self):
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.name = 'vsan'
            self.assertEqual(
                'The command " vsan database ; vsan ' + str(i) + ' name \'vsan\' " gave the error " vsan ' + str(
                    i) + ':vsan(s) reserved ".', str(e.exception))
