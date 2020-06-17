from mdssdk.switch import Switch
from mdssdk.devicealias import DeviceAlias

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

# Instantiating DeviceAlias object
d = DeviceAlias(sw)

# Display the database, mode, distribute, locked
print("Device Alias Database")
print(d.database)
print("Mode : " + d.mode)
print("Distribute : " + str(d.distribute))
print("Locked : " + str(d.locked))

old = d.database
d.clear_database()

# Adding new device alias
new = {"device1": "21:00:00:0e:1e:30:34:a5", "device2": "21:00:00:0e:1e:30:3c:c5"}
d.create(new)

prnt("Clearing database\nDatabase after adding new entry")
print(d.database)

# Renaming the device alias
d.rename("device1", "device_new_name")

print("Database after renaming device alias device1 as device_new_name")
print(d.database)

# Deleting device alias
d.delete("device_new_name")
d.delete("device2")

# Recreating original database
d.create(old)
