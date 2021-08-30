from mdssdk.switch import Switch
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone

user = "yourswitchusername"
pw = "yourswitchpassword"
ip_address = "yourswitchip"  # 10.197.155.110
p = 8443

# Set connection_type='https' for NXAPI
# Set connection_type='ssh' for SSH
sw = Switch(
    ip_address=ip_address,
    username=user,
    password=pw,
    connection_type="https",
    port=p,
    timeout=30,
    verify_ssl=False,
)

# Instantiating Vsan object with id 2
v = Vsan(sw, 2)

# Creating vsan
v.create()

# Instantiate zone object
z = Zone(sw, "zone1", v.id)

# Create new zone
z.create()

memlist = [
    {"pwwn": "50:08:01:60:08:9f:4d:00"},
    {"ip-address": "1.1.1.1"},
    {"symbolic-nodename": "symbnodename"},
    {"fwwn": "11:12:13:14:15:16:17:18"},
    {"fcid": "0x123456"},
]

# Adding members to zone
z.add_members(memlist)

# Display zone name, vsan id, members
print("Zone name: " + z.name)
print("Vsan id: " + str(z.vsan.id))
print("Zone members: " + str(z.members))

# Removing members from zone
z.remove_members(memlist)

# Deleting zone
z.delete()

# Deleting vsan
v.delete()
