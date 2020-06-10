from mdssdk.switch import Switch

user = 'yourswitchusername'
pw = 'yourswitchpassword'
ip_address = 'yourswitchip'  # 10.197.155.110
p = 8443

# Set connection_type='https' for NXAPI
# Set connection_type='ssh' for SSH
switch_obj = Switch(ip_address=ip_address, username=user, password=pw, connection_type='https', port=p, timeout=30,
            verify_ssl=False)

# Displaying switch name, version, image
print("Name: "+switch_obj.name)
print("Version: "+switch_obj.version)
print("Kickstart Image: "+switch_obj.kickstart_image)
print("System Image: "+switch_obj.system_image)

# Changing name of switch
switch_obj.name = "switch_test"
print("Changed Name: "+switch_obj.name)

# Enabling feature analytics
switch_obj.feature('analytics', True)
print("Analytics feature : "+str(switch_obj.feature('analytics')))
