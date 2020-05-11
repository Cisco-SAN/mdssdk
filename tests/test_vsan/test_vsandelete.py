import unittest

from mdssdk.vsan import Vsan
from mdssdk.connection_manager.errors import CLIError


class TestVsanDelete(unittest.TestCase):

    def test_delete(self):
        i = self.delete_id
        v = Vsan(switch=self.switch, id=i)
        if v.id is None:
            v.create()
        self.assertEqual(i, v.id)
        v.delete()
        self.assertIsNone(v.id)

    def test_delete_default_vsan(self):
        i = self.default_id
        v = Vsan(switch=self.switch, id=i)
        with self.assertRaises(CLIError) as e:
            v.delete()
        self.assertEqual(
            'The command " terminal dont-ask ; vsan database ; no vsan ' + str(i) + ' " gave the error " vsan ' + str(
                i) + ':cannot delete default vsan ".', str(e.exception))

    def test_delete_nonexistingvsan(self):
        i = self.nonexisting_id
        v = Vsan(switch=self.switch, id=i)
        if v.id is not None:
            v.delete()
        with self.assertRaises(CLIError) as e:
            v.delete()
        self.assertEqual(
            'The command " terminal dont-ask ; vsan database ; no vsan ' + str(i) + ' " gave the error " vsan ' + str(
                i) + ':vsan not configured ".', str(e.exception))

    def test_delete_boundary(self):
        for i in self.boundary_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.delete()
            self.assertEqual('The command " terminal dont-ask ; vsan database ; no vsan ' + str(
                i) + ' " gave the error " % Invalid command ".', str(e.exception))

    def test_delete_reserved(self):
        for i in self.reserved_id:
            v = Vsan(switch=self.switch, id=i)
            with self.assertRaises(CLIError) as e:
                v.delete()
            self.assertEqual('The command " terminal dont-ask ; vsan database ; no vsan ' + str(
                i) + ' " gave the error " vsan ' + str(i) + ':vsan(s) reserved ".', str(e.exception))
