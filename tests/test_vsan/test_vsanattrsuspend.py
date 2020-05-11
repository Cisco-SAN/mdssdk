import unittest
from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanAttrSuspend(unittest.TestCase):

    def test_suspend_write(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[0])
        v.create()
        v.suspend = True
        self.assertEqual("suspended", v.state)
        v.suspend = False
        self.assertEqual("active", v.state)
        v.delete()

    def test_suspend_read(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[1])
        v.create()
        with self.assertRaises(AttributeError) as e:
            print(v.suspend)
        self.assertEqual("unreadable attribute", str(e.exception))
        v.delete()

    def test_suspend_write_nonexistingvsan(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[2])
        if v.id is not None:
            v.delete()
        v.suspend = True
        self.assertEqual("suspended", v.state)
        v.delete()

    def test_suspend_write_boundary(self):
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.suspend = True
            self.assertEqual(
                'The command " vsan database ; vsan ' + str(i) + ' suspend " gave the error " % Invalid command ".',
                str(e.exception))

    def test_suspend_write_reserved(self):
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.suspend = True
            self.assertEqual('The command " vsan database ; vsan ' + str(i) + ' suspend " gave the error " vsan ' + str(
                i) + ':vsan(s) reserved ".',
                             str(e.exception))

    def test_suspend_write_invalid(self):
        v = Vsan(switch=self.switch, id=self.vsan_id[3])
        v.create()
        with self.assertRaises(TypeError) as e:
            v.suspend = "asdf"
        self.assertEqual("Only bool value(true/false) supported.", str(e.exception))
        v.delete()
