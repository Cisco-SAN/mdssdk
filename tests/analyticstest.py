import logging
from pprint import pprint as print

from mdssdk.switch import Switch

logging.basicConfig(
    filename="anatest.log",
    filemode="w",
    level=logging.DEBUG,
    format="[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s",
)

# scsi profiles
port_scsi_profile = {"protocol": "scsi", "metrics": [], "view": "port"}
logical_port_scsi_profile = {"protocol": "scsi", "metrics": [], "view": "logical_port"}
app_scsi_profile = {"protocol": "scsi", "metrics": [], "view": "app"}
scsi_target_profile = {"protocol": "scsi", "metrics": [], "view": "scsi_target"}
scsi_initiator_profile = {"protocol": "scsi", "metrics": [], "view": "scsi_initiator"}
scsi_target_app_profile = {"protocol": "scsi", "metrics": [], "view": "scsi_target_app"}
scsi_initiator_app_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_initiator_app",
}
scsi_target_tl_flow_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_target_tl_flow",
}
scsi_target_it_flow_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_target_it_flow",
}
scsi_initiator_it_flow_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_initiator_it_flow",
}
scsi_target_itl_flow_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_target_itl_flow",
}
scsi_initiator_itl_flow_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_initiator_itl_flow",
}
scsi_target_io_profile = {"protocol": "scsi", "metrics": [], "view": "scsi_target_io"}
scsi_initiator_io_profile = {
    "protocol": "scsi",
    "metrics": [],
    "view": "scsi_initiator_io",
}

sw = Switch(
    ip_address="10.126.94.184",
    username="admin",
    password="nbv!2345",
    connection_type="https",
    port=8443,
    timeout=30,
    verify_ssl=False,
)
# sw.feature("analytics", True)
analytics_object = sw.analytics
analytics_object.create_query("scsi_target_io_profile", scsi_target_io_profile)
show_scsi_initiator_query = analytics_object.show_query("scsi_target_io_profile")
analytics_object.delete_query("scsi_target_io_profile")
analytics_object.create_query("port_query", port_scsi_profile)
show_port_query = analytics_object.show_query("port_query")
print("Checking Packet count")
print(show_port_query)
for item in show_port_query[0]:
    if "total_write_io_count" in item:
        print(item)
analytics_object.delete_query("port_query")
