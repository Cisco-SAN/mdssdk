from mdssdk.devicealias import DeviceAlias
from mdssdk.fc import Fc
from mdssdk.portchannel import PortChannel
from mdssdk.switch import Switch
from mdssdk.vsan import Vsan
from mdssdk.zone import Zone
from mdssdk.zoneset import ZoneSet

# Switch credentials
user = "yourswitchusername"
pw = "yourswitchpassword"
ip_address = "yourswitchip"  # 10.197.155.110
p = 8443

# Creating switch object
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

# Creating Fc object for interface fc1/3
int13 = Fc(sw, "fc1/3")

# Instantiating PortChannel object 1
pc1 = PortChannel(sw, 1)

# Creating port channel
pc1.create()

# Adding interfaces to vsan 2
v.add_interfaces([int13, pc1])

# Instantiating DeviceAlias object
d = DeviceAlias(sw)
new = {"da1": "60:66:61:01:0e:00:01:ff"}

# Adding new device alias
d.create(new)

# Instantiate zone object
z = Zone(sw, "zone1", v.id)

# Create new zone
z.create()

# Configuring fcalias
sw.config("fcalias name somefcalias vsan " + str(v.id))

memlist = [
    {"pwwn": "50:08:01:60:08:9f:4d:00"},
    {"pwwn": "50:08:01:60:08:9f:4d:01"},
    {"interface": int13.name},
    {"device-alias": "da1"},
    {"ip-address": "1.1.1.1"},
    {"symbolic-nodename": "symbnodename"},
    {"fwwn": "11:12:13:14:15:16:17:18"},
    {"fcid": "0x123456"},
    {"interface": pc1.name},
    {"symbolic-nodename": "testsymnode"},
    {"fcalias": "somefcalias"},
]

# Adding members to zone
z.add_members(memlist)

# Instantiating ZoneSet object
zoneset = ZoneSet(sw, "zoneset1", v.id)

# Creating zoneset
zoneset.create()

# Add members to zoneset
zoneset.add_members([z])

# Activating zoneset
zoneset.activate(True)

# Display zoneset information
print("Zoneset name: " + zoneset.name)
print("Vsan id: " + str(zoneset.vsan.id))
print("Zoneset members: " + str(zoneset.members))
print("Activation: " + zonese.is_active())

# Removing members from zoneset
zoneset.remove_members([z])

# Deleting zoneset
zoneset.delete()

# Removing members from zone
z.remove_members(memlist)

# Deleting zone
z.delete()

# Deleting vsan
v.delete()

# Deleting device alias
d.delete("da1")

# Deleting port channel
pc1.delete()
