# An example to show how we can do multiprocessing to execute some logic on multiple switches parallelly

from mdssdk.switch import Switch
from concurrent.futures import wait
from concurrent.futures.thread import ThreadPoolExecutor
import multiprocessing

user = "your_switch_username"
pw = "your_switch_password"
iplist = ["ip1", "ip2"]
p = 8443

myData = {}


def runAnySwitchLogic(ip, user, pw, port):
    my_switch = Switch(ip, user, pw, "https", port=port, verify_ssl=False)
    status = isCFSoIpEnabled(my_switch)
    myData[my_switch.name] = status


def isCFSoIpEnabled(sw):
    cmd = "show cfs status"
    # ensures that the output is in cli output format
    out = sw.show(cmd, raw_text=True)
    if "Distribution over IP : Disabled" in out:
        return "Disabled"
    return "Enabled"


m = multiprocessing.Manager()
allfutures = []
executor = ThreadPoolExecutor(len(iplist))
IP_list = []
CFS_list = []

for i in range(0, len(iplist)):
    ip = iplist[i]
    fut = executor.submit(runAnySwitchLogic, ip, user, pw, p)
    allfutures.append(fut)
wait(allfutures)

for swname, cfsstatus in myData.items():
    print('CFS Distribution over IP on switch', swname, 'is', cfsstatus)
