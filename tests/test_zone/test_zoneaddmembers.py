import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone


class TestZoneAddMembers(unittest.TestCase):

    def test_add_members_dict(self):
        i = self.vsan_id[0]
        v = Vsan(self.switch, i)
        v.create()
        z = Zone(self.switch, v, self.zone_name[0])
        z.create()
        members = self.members_dict
        self.switch.config('fcalias name somefcalias vsan ' + str(i))
        z.add_members(members)
        log.debug("Zone Members : " + str(members))
        log.debug("Zone Members : " + str(z.members))
        self.assertEqual(len(members), len(z.members))
        z.delete()
        v.delete()

    def test_add_members(self):
        v = Vsan(self.switch, self.vsan_id[1])
        v.create()
        z = Zone(self.switch, v, self.zone_name[1])
        z.create()
        members = self.members_list
        z.add_members(members)
        self.assertEqual(len(members), len(z.members))
        log.debug("Zone Members : " + str(z.members))
        z.delete()
        v.delete()

    def test_add_members_error_pwwn(self):
        i = self.vsan_id[2]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name[2]
        z = Zone(self.switch, v, name)
        z.create()
        members = [{'pwwn': '50:08:01:60:08:9f:4d:00:01'}]
        with self.assertRaises(CLIError) as e:
            z.add_members(members)
        self.assertEqual('The command " zone name ' + str(name) + ' vsan ' + str(
            i) + ' ; member pwwn 50:08:01:60:08:9f:4d:00:01 " gave the error " % Invalid command ".', str(e.exception))
        z.delete()
        v.delete()

    def test_add_members_error_ip(self):
        i = self.vsan_id[3]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name[3]
        z = Zone(self.switch, v, name)
        z.create()
        members = [{'ip-address': '1.1.1.1.1'}]
        with self.assertRaises(CLIError) as e:
            z.add_members(members)
        self.assertEqual('The command " zone name ' + str(name) + ' vsan ' + str(
            i) + ' ; member ip-address 1.1.1.1.1 " gave the error " % Invalid ip address ".', str(e.exception))
        z.delete()
        v.delete()

    def test_add_members_error_fcid(self):
        i = self.vsan_id[4]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name[4]
        z = Zone(self.switch, v, name)
        z.create()
        members = [{'fcid': '0x123'}]
        with self.assertRaises(CLIError) as e:
            z.add_members(members)
        self.assertEqual('The command " zone name ' + str(name) + ' vsan ' + str(
            i) + ' ; member fcid 0x123 " gave the error " Invalid FCID ".', str(e.exception))
        z.delete()
        v.delete()

    def test_add_members_error_fwwn(self):
        i = self.vsan_id[5]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name[5]
        z = Zone(self.switch, v, name)
        z.create()
        members = [{'fwwn': '11:12:13:14:15:16:17:18:19'}]
        with self.assertRaises(CLIError) as e:
            z.add_members(members)
        self.assertEqual('The command " zone name ' + str(name) + ' vsan ' + str(
            i) + ' ; member fwwn 11:12:13:14:15:16:17:18:19 " gave the error " % Invalid command ".', str(e.exception))
        z.delete()
        v.delete()

    def test_add_members_error_fcalias(self):
        i = self.vsan_id[6]
        v = Vsan(self.switch, i)
        v.create()
        name = self.zone_name[6]
        z = Zone(self.switch, v, name)
        z.create()
        members = [{'fcalias': 'somefcalias'}]
        with self.assertRaises(CLIError) as e:
            z.add_members(members)
        self.assertEqual('The command " zone name ' + str(name) + ' vsan ' + str(
            i) + ' ; member fcalias somefcalias " gave the error " Alias not present ".', str(e.exception))
        z.delete()
        v.delete()
