import unittest

from mdssdk.zone import Zone
from mdssdk.vsan import Vsan, VsanNotPresent
from mdssdk.connection_manager.errors import CLIError


class TestZoneCreate(unittest.TestCase):

    def test_nonexistingvsan(self):
        i = self.vsan_id[0]
        v = Vsan(self.switch, i)
        if v.id is not None:
            v.delete()
        with self.assertRaises(VsanNotPresent) as e:
            z = Zone(self.switch, v, "z1")
        self.assertEqual(
            "VsanNotPresent: Vsan " + str(i) + " is not present on the switch. Please create the vsan first.",
            str(e.exception))

    def test_create(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        zonename = self.zone_name[0]
        z = Zone(self.switch, v, zonename)
        z.create()
        self.assertEqual(zonename, z.name)
        z.delete()
        v.delete()

    def test_create_name_invalid(self):
        i = self.vsan_id[2]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name_invalid
        z = Zone(self.switch, v, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zone name " + str(name) + " vsan " + str(
            i) + " \" gave the error \" Illegal character present in the name \".", str(e.exception))
        v.delete()

    def test_create_name_invalidfirstchar(self):
        i = self.vsan_id[3]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name_invalidfirstchar
        z = Zone(self.switch, v, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zone name " + str(name) + " vsan " + str(
            i) + " \" gave the error \" Illegal first character (name must start with a letter) \".", str(e.exception))
        v.delete()

    def test_create_name_beyondmax(self):
        i = self.vsan_id[4]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name_beyondmax
        z = Zone(self.switch, v, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.maxDiff = 1000
        self.assertEqual("The command \" zone name " + str(name) + " vsan " + str(
            i) + " \" gave the error \" % String exceeded max length of (64) \".", str(e.exception))
        v.delete()

    def test_create_name_max(self):
        v = Vsan(self.switch, self.vsan_id[5])
        v.create()
        name = self.zone_name_max
        z = Zone(self.switch, v, name)
        z.create()
        self.assertEqual(name, z.name)
        z.delete()
        v.delete()
