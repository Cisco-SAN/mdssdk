from mdssdk.switch import Switch
from mdssdk.vsan import Vsan

user = 'yourswitchusername'
pw = 'yourswitchpassword'
ip_address = 'yourswitchip'  # 10.197.155.110
p = 8443

# Set connection_type='https' for NXAPI
# Set connection_type='ssh' for SSH
sw = Switch(ip_address=ip_address, username=user, password=pw, connection_type='https', port=p, timeout=30,
            verify_ssl=False)

# Example for creating and deleting 10 vsan objects from id 10 to 19
vsan = []
for i in range(10, 20):
    vsan.append(Vsan(switch=sw, id=1))
    print("Vsan ID\tName\tState")
    for v in vsan:
        v.create()  # creates vsan on switch
        print(str(v.id) + "\t\t" + v.name + "\t" + v.state)  # print id,name,state
        v.delete()  # deletes vsan
