from mdssdk.switch import Switch
import json
import time
from pprint import pprint


def dump(obj):
    for attr in dir(obj):
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


sw = Switch('10.126.94.216', 'admin', 'nbv!2345', connection_type='ssh', verify_ssl=False)

# out = sw.show("show fcns database detail vsan 50")
# print(out)
# print(len(out))
i = 0
while True:
    cmd = "ivr zoneset name IVR_Zoneset1 ; member zKess" + str(i)
    print(cmd)
    i = i + 1
    sw.config(cmd)
    if i == 1023:
        break
exit()


# sw = Switch('10.197.106.40', 'admin', 'nbv_!2345', connection_type='ssh')
# print(sw.version)


def checkACLCC(sw):
    count = 1
    while True:
        print("Checking ACL consistency checker.." + str(count))
        ccpassed = True
        out = sw.show("show consistency-checker acl-table-status")
        for eachline in out:
            if "FAIL" in eachline:
                ccpassed = False
                if count == 20:
                    print('\n'.join(out))
                    print("FAILED!!! Please check the setup")
                    exit()
                else:
                    count = count + 1
                    time.sleep(10)
                    break
        if ccpassed:
            break

    print("ACL consistency checker.. PASS")


def counters(sw, ipsint, fcipint):
    allint = ', '.join(ipsint)
    out = sw.show("show interface " + allint + " counters brief")
    print('\n'.join(out))

    allint = ', '.join(fcipint)
    out = sw.show("show interface " + allint + " counters brief")
    print('\n'.join(out))


def clearPktDrops(sw):
    out = sw.show("clrdrops")


def showPktDrops(sw):
    out = sw.show("pktdrops")
    print("PktDrops: ")
    print(out)


ipsint = ['ips1/1', 'ips1/2', 'ips1/3', 'ips1/4']
fcipint = ['fcip4', 'fcip5', 'fcip6', 'fcip10', 'fcip11', 'fcip12', 'fcip30', 'fcip31', 'fcip32', 'fcip40', 'fcip41',
           'fcip42']

clearPktDrops(sw)
counter = 0
while True:
    counters(sw, ipsint, fcipint)
    counter = counter + 1
    print("------------------- Iteration ---------- " + str(counter))
    checkACLCC(sw)
    interfaces = ipsint + fcipint
    # interfaces = fcipint
    for intf in interfaces:
        print("Shutting down.................... " + intf)
        sw.config("interface " + intf + " ;  shutdown")
        time.sleep(0.5)
        checkACLCC(sw)
        print("Bringing up....................... " + intf)
        sw.config("interface " + intf + " ; no shutdown")
        time.sleep(0.5)
        checkACLCC(sw)
        counters(sw, ipsint, fcipint)
    # interfaces = sw.interfaces
    # #print(interfaces)
    # for fcint,fcintObj in interfaces.items():
    #     print(fcint + " " +  fcintObj.status)
    #     print(fcint + " " + json.dumps(fcintObj.counters.brief))
    # showPktDrops(sw)
    #
    # for fcint,fcintObj in interfaces.items():
    #     if 'fc' in fcint and fcintObj.status == 'trunking':
    #         print("bringing down " + fcint)
    #         fcintObj.status = "shutdown"
    #         time.sleep(0.5)
    #         print(fcint + " " + fcintObj.status)
    #         showPktDrops(sw)
    #         checkACLCC(sw)
    #         print("bringing up " + fcint)
    #         fcintObj.status = "no shutdown"
    #         time.sleep(0.5)
    #         print(fcint + " " + fcintObj.status)
    #         print(fcint + " " + json.dumps(fcintObj.counters.brief))
    #         showPktDrops(sw)
    #         checkACLCC(sw)
