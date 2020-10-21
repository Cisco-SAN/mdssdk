import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from tests.test_zone.vars import *

log = logging.getLogger(__name__)


class TestZoneRemoveMembers(unittest.TestCase):
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

    def test_remove_members_dict(self):
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
        self.assertIsNotNone(self.z.members)
        self.z.remove_members(members)
        self.assertEqual([], self.z.members)
        d.delete(da_name)

    def test_remove_members_list(self):
        members = []
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
        self.assertIsNotNone(self.z.members)
        self.z.remove_members(members)
        self.assertEqual([], self.z.members)
        self.z.delete()

    def test_remove_members_notpresent(self):
        members = ["10:99:88:90:76:88:99:ef"]
        self.assertEqual([], self.z.members)
        with self.assertRaises(CLIError) as e:
            self.z.remove_members(members)
        self.assertIn("Member not present", str(e.exception))
        self.z.delete()

    # def test_remove_members_zone_notpresent(self):
    #     self.z.delete()
    #     members = ["10:99:88:90:76:88:99:ef"]
    #     # TODO: Was working in 8.4.2a not in 8.4.2b (CSCvv59174)
    #     # with self.assertRaises(CLIError) as e:
    #     #     self.z.remove_members(members)
    #     # self.assertIn("Zone not present", str(e.exception))

    def tearDown(self) -> None:
        self.v.delete()
