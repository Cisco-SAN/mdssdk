import logging

logging.basicConfig(filename='test.log', filemode='w', level=logging.DEBUG,
                    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s")

from mdssdk.switch import Switch
from mdssdk.devicealias import DeviceAlias
import os

print(os.environ['NET_TEXTFSM'])

user = "admin"
pw = "nbv!2345"
sw = Switch("10.126.94.110", user, pw, connection_type="ssh", verify_ssl=False)
# ('device-alias database  ; device-alias name da1& pwwn 52:66:61:01:0e:00:01:ff', 'Illegal character present in the name\n')
d = DeviceAlias(sw)
d.mode = "basic"
# print("Changing name to sw110Mini")
# sw.name = "switch12345678912345678912345678"
# print("----")
# print(sw.zones)


# sw = Switch("10.126.94.184",user,pw,connection_type="https",verify_ssl=False)
# print(sw.modules)

# v = Vsan(switch=sw, id=1)
# v.create()
# name = "vsan\?123"
# v.name = name
# sw1 = Switch("10.126.94.129",user,pw,connection_type="ssh")
# for sw in [sw,sw1]:
#     print(sw.ipaddr)
#     print(sw.version)
#     print(sw.model)
#     print(sw.kickstart_image)
#     print(sw.system_image)
#     print(sw.form_factor)
#     print(sw.type)
#     print(sw.name)
#     # pc = PortChannel(sw, 1)
#     # print(pc.id)
#     # print(pc.description)
#     # print(pc.mode)
#     # print(pc.name)
#
# sw = Switch("10.126.94.121",user,pw,connection_type="https",verify_ssl=False)
# sw1 = Switch("10.126.94.129",user,pw,connection_type="https",verify_ssl=False)
# for sw in [sw,sw1]:
#     print(sw.ipaddr)
#     print(sw.version)
#     print(sw.model)
#     print(sw.kickstart_image)
#     print(sw.system_image)
#     print(sw.form_factor)
#     print(sw.type)
#     print(sw.name)
#
# #
# # Get a separate analytics handler per switch
# anaHandler = sw.analytics
#
# # Create a query(install query)
# #anaHandler.create_query(name="port_nvme_query", profile=nvme_profile, clear=True, differential=True,interval=45)
#
# # install query result
# #anaHandler.show_query(name="port_query")
#
# # pull query result, same API as above but here we pass profile instead of name
# #anaHandler.show_query(profile=scsi_profile_few, clear=True, differential=True)
#
# # purge
# #anaHandler.purge(profile=scsi_profile)
#
# # clear
# #anaHandler.clear(profile=scsi_profile)
#
# # Delete a query(install query)
# #anaHandler.delete_query(name="port_nvme_query")
#
# # Now comes all APIs for “show analytics npu-load”
#
# # NPU load details
#
# # scsi NPU load on mod 1
# print(anaHandler.npu_load(module=1, protocol='scsi'))
#
# # nvme NPU load on mod 1
# print(anaHandler.npu_load(module=1, protocol='nvme'))
#
# # total NPU load on mod 1
# # This info can be got from "show port-sampling module <>” or
# # we could just call the above 2 APIs and add up
# print(anaHandler.npu_load(module=1))
#
# # ITLs/ITNs details
#
# # scsi ITLs for mod 1
# print(anaHandler.itls(module=1))
#
# # nvme ITNs for mod 1
# print(anaHandler.itns(module=1))
#
# # total ITs(scsi+nvme) on mod 1
# print(anaHandler.itls_itns(module=1))
#
# # scsi ITLs on entire switch
# print(anaHandler.itls())
#
# # nvme ITNs on entire switch
# print(anaHandler.itns())
#
# # total ITs(scsi+nvme) on entire switch
# print(anaHandler.itls_itns())
#
# # Initiator details per module
# # ============================
#
# # scsi initiators for mod 1
# print(anaHandler.initiators(module=1, protocol='scsi'))
#
# # nvme initiators for mod 1
# print(anaHandler.initiators(module=1, protocol='nvme'))
#
# # total initiators(scsi+nvme) on mod 1
# print(anaHandler.initiators(module=1))
#
# # Initiator details entire switch
# # ===============================
#
# # scsi initiators on entire switch
# print(anaHandler.initiators(protocol='scsi'))
#
# # nvme initiators on entire switch
# print(anaHandler.initiators(protocol='nvme'))
#
# # total initiators(scsi+nvme) on entire switch
# print(anaHandler.initiators())
#
# # Target details per module
# # ===============================
#
# # scsi targets for mod 1
# print(anaHandler.targets(module=1, protocol='scsi'))
#
# # nvme targets for mod 1
# print(anaHandler.targets(module=1, protocol='nvme'))
#
# # total targets(scsi+nvme) on mod 1
# print(anaHandler.targets(module=1))
#
# # Target details entire switch
# # ===============================
#
# # scsi targets on entire switch
# print(anaHandler.targets(protocol='scsi'))
#
# # nvme targets on entire switch
# print(anaHandler.targets(protocol='nvme'))
#
# # total targets(scsi+nvme) on entire switch
# print(anaHandler.targets())
#
