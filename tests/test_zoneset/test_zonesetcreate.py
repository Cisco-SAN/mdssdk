import unittest

from mdssdk.zoneset import ZoneSet
from mdssdk.vsan import Vsan, VsanNotPresent
from mdssdk.connection_manager.errors import CLIError


class TestZoneSetCreate(unittest.TestCase):

    def test_nonexistingvsan(self):
        i = self.vsan_id[0]
        v = Vsan(self.switch, i)
        if v.id is not None:
            v.delete()
        with self.assertRaises(VsanNotPresent) as e:
            z = ZoneSet(self.switch, v, self.zoneset_name[0])
        self.assertEqual("VsanNotPresent: Vsan " + str(i) + " is not present on the switch.", str(e.exception))

    def test_create(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        name = self.zoneset_name[1]
        z = ZoneSet(self.switch, v, name)
        z.create()
        self.assertEqual(name, z.name)
        z.delete()
        v.delete()

    def test_create_name_invalid(self):
        i = self.vsan_id[2]
        v = Vsan(self.switch, i)
        v.create()
        invalid = self.zoneset_name_invalid
        z = ZoneSet(self.switch, v, invalid)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zoneset name " + str(invalid) + " vsan " + str(
            i) + " \" gave the error \" Illegal character present in the name \".", str(e.exception))
        v.delete()

    def test_create_name_invalidfirstchar(self):
        i = self.vsan_id[3]
        v = Vsan(self.switch, i)
        v.create()
        invalid = self.zoneset_name_invalidfirstchar
        z = ZoneSet(self.switch, v, invalid)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual("The command \" zoneset name " + str(invalid) + " vsan " + str(
            i) + " \" gave the error \" Illegal first character (name must start with a letter) \".", str(e.exception))
        v.delete()

    def test_create_name_beyondmax(self):
        i = self.vsan_id[4]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zoneset_name_beyondmax
        z = ZoneSet(self.switch, v, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.maxDiff = 1000
        self.assertEqual("The command \" zoneset name " + name + " vsan " + str(
            i) + " \" gave the error \" % String exceeded max length of (64) \".", str(e.exception))
        v.delete()

    def test_create_name_max(self):
        v = Vsan(self.switch, self.vsan_id[5])
        v.create()
        name = self.zoneset_name_max
        z = ZoneSet(self.switch, v, name)
        z.create()
        self.assertEqual(name, z.name)
        z.delete()
        v.delete()

    def test_create_max(self):
        i = self.vsan_id[6]
        v = Vsan(self.switch, i)
        v.create()
        # success case
        for i in self.zoneset_max_range:
            name = "zone" + str(i)
            z = ZoneSet(self.switch, v, name)
            z.create()
            self.assertEqual(name, z.name)
        # failure case
        name = "zs"
        z = ZoneSet(self.switch, v, name)
        with self.assertRaises(CLIError) as e:
            z.create()
        self.assertEqual('The command " zoneset name ' + str(name) + ' vsan ' + str(
            i) + ' " gave the error " cannot create the zoneset; maximum possible number of zonesets is already configured ".',
                         str(e.exception))

        v.delete()

    # same zoneset name different vsans
    def test_create_same_name(self):
        v7 = Vsan(self.switch, self.vsan_id[7])
        v7.create()
        v8 = Vsan(self.switch, self.vsan_id[8])
        v8.create()

        name = self.zoneset_name[2]
        z7 = ZoneSet(self.switch, v7, name)
        z7.create()
        self.assertEqual(name, z7.name)
        z8 = ZoneSet(self.switch, v8, name)
        z8.create()
        self.assertEqual(name, z8.name)

        v7.delete()
        v8.delete()
