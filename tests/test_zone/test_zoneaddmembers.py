import unittest
import logging

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneAddMembers(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.v.create()
        self.z = Zone(self.switch, "test_zone", self.id)
        self.z.create()

    # def test_add_members_zone_notpresent(self):
    #     self.z.delete()
    #     members = ["10:99:88:90:76:88:99:ef"]
    #     # TODO: Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
    #     #with self.assertRaises(CLIError) as e:
    #     #    self.z.add_members(members)
    #     #self.assertIn("Zone not present", str(e.exception))

    def test_add_members_dict(self):
        fc_name = ""
        for k, v in list(self.switch.interfaces.items()):
            if type(v) is Fc:
                fc_name = k
                break
        while True:
            pc_id = get_random_id(1, 256)
            if "port-channel" + str(pc_id) not in self.switch.interfaces.keys():
                break
        pc = PortChannel(self.switch, pc_id)
        d = DeviceAlias(self.switch)
        olddb = d.database
        if olddb is None:
            da_name = get_random_string()
            da_pwwn = get_random_pwwn()
        else:
            while True:
                da_name = get_random_string()
                da_pwwn = get_random_pwwn()
                if da_name not in olddb.keys() and da_pwwn not in olddb.values():
                    break
        d.create({da_name: da_pwwn})
        members = [
            {"pwwn": "50:08:01:60:08:9f:4d:00"},
            {"interface": fc_name},
            {"device-alias": da_name},
            {"ip-address": "1.1.1.1"},
            {"symbolic-nodename": "symbnodename"},
            {"fwwn": "11:12:13:14:15:16:17:18"},
            {"fcid": "0x123456"},
            {"interface": pc.name},
            {"fcalias": "somefcalias"},
        ]
        self.switch.config("fcalias name somefcalias vsan " + str(self.id))
        self.z.add_members(members)
        mem = self.z.members
        d.delete(da_name)
        log.debug("Zone Members To Add : " + str(members))
        log.debug("Zone Members Added : " + str(mem))
        self.assertEqual(len(members), len(mem))

    def test_add_members(self):
        members = []
        # print(self.switch.interfaces)
        for v in list(self.switch.interfaces.values()):
            if type(v) is Fc:
                members.append(v)
                break
        while True:
            pc_id = get_random_id(1, 256)
            if "port-channel" + str(pc_id) not in self.switch.interfaces.keys():
                break
        members.append(PortChannel(self.switch, pc_id))
        members.append("10:99:88:90:76:88:99:ef")
        self.z.add_members(members)
        log.debug("Zone Members To Add : " + str(members))
        log.debug("Zone Members Added : " + str(self.z.members))
        self.assertEqual(len(members), len(self.z.members))

    def test_add_members_error_pwwn(self):
        members = [{"pwwn": "50:08:01:60:08:9f:4d:00:01"}]
        with self.assertRaises(CLIError) as e:
            self.z.add_members(members)
        self.assertEqual(
            'The command " zone name test_zone vsan '
            + str(self.id)
            + ' ; member pwwn 50:08:01:60:08:9f:4d:00:01 " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def test_add_members_error_ip(self):
        members = [{"ip-address": "1.1.1.1.1"}]
        with self.assertRaises(CLIError) as e:
            self.z.add_members(members)
        self.assertEqual(
            'The command " zone name test_zone vsan '
            + str(self.id)
            + ' ; member ip-address 1.1.1.1.1 " gave the error " % Invalid ip address ".',
            str(e.exception),
        )

    def test_add_members_error_fcid(self):
        members = [{"fcid": "0x123"}]
        with self.assertRaises(CLIError) as e:
            self.z.add_members(members)
        self.assertEqual(
            'The command " zone name test_zone vsan '
            + str(self.id)
            + ' ; member fcid 0x123 " gave the error " Invalid FCID ".',
            str(e.exception),
        )

    def test_add_members_error_fwwn(self):
        members = [{"fwwn": "11:12:13:14:15:16:17:18:19"}]
        with self.assertRaises(CLIError) as e:
            self.z.add_members(members)
        self.assertEqual(
            'The command " zone name test_zone vsan '
            + str(self.id)
            + ' ; member fwwn 11:12:13:14:15:16:17:18:19 " gave the error " % Invalid command ".',
            str(e.exception),
        )

    def test_add_members_error_fcalias(self):
        members = [{"fcalias": "somefcalias"}]
        with self.assertRaises(CLIError) as e:
            self.z.add_members(members)
        self.assertEqual(
            'The command " zone name test_zone vsan '
            + str(self.id)
            + ' ; member fcalias somefcalias " gave the error " Alias not present ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        self.v.delete()
