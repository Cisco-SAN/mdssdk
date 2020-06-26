from mdssdk.switch import Switch

user = "yourswitchusername"
pw = "yourswitchpassword"
ip_address = "yourswitchip"  # 10.197.155.110
p = 8443

# Set connection_type='https' for NXAPI
# Set connection_type='ssh' for SSH
switch_obj = Switch(
    ip_address=ip_address,
    username=user,
    password=pw,
    connection_type="https",
    port=p,
    timeout=30,
    verify_ssl=False,
)

# Print the information of all switch modules
mod_handler = switch_obj.modules  # dict of module objects
print(mod_handler)
for m in mod_handler.values():
    print("Model : " + m.model)
    print("Module Number : " + str(m.module_number))
    print("Ports : " + str(m.ports))
    print("Status : " + m.status)
    print("Type : " + m.type)
