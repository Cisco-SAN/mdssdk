# 13cmx18cm
# 5.11811x7.08661
# 15.5cmx20.5cm
# 6.102362x8.070866


from mdssdk.fabric import Fabric
from mdssdk.switch import Switch
from prettytable import PrettyTable
import utils
from switch_details import SwitchDetails
from do_checks import Do_Checks
import threading
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
import logging
import time

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)
logFileFormatter = logging.Formatter(
    "[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s"
)
logConsoleFormatter = logging.Formatter(
    "[%(asctime)s] %(message)s"
)
logging.getLogger("paramiko").setLevel(logging.WARNING)
# Add stdout handler, with level INFO
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logConsoleFormatter)
logging.getLogger().addHandler(console)

# Add file handler, with level DEBUG
fileHandler = logging.FileHandler("install_script.log", mode='w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFileFormatter)
logging.getLogger().addHandler(fileHandler)

log = logging.getLogger(__name__)

import sys

sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=150))

utils.banner("Starting install script for the entire fabric")
START = time.perf_counter()

y = PrettyTable()
y.field_names = ["Switch Name", "IP Address", "Version"]
y.sortby = "IP Address"
x = PrettyTable()
x.field_names = ["Switch Name", "IP Address", "Version", "NPV?", "Status"]
x.sortby = "IP Address"
x.align = 'l'

swip = utils.askIP()
uname = utils.askUser()
pw = utils.askPassword()
npv_req = utils.askNPV()
upgver = utils.askVersionUpgrade()
pc = utils.askForPrePostCheck()
print("\n")

log.debug("Seed Ip: " + swip)
log.debug("uname: " + uname)
log.debug("npv req: " + str(npv_req))
# print("npv req: " + str(npv_req))
log.debug("upgver: " + upgver)
log.info("Discovering fabric.. Please wait..")
try:
    s = Switch(swip, uname, pw, connection_type='ssh')
except Exception as e:
    print("ERROR!! Could not connect to the seed switch via ssh. Please check the connection.")
    log.exception(e)
    exit()

if s.npv:
    msg = "ERROR!! Cannot discover fabric using NPV switch. Please give an NPIV address"
    print(msg)
    log.debug(msg)
    exit()

f1 = Fabric(swip, uname, pw, connection_type='ssh')
f1.all_switches_in_fabric(discover_npv=npv_req)

allsws = f1.switches
swdetail_list = []
swdetail_upgrade = []
for swip, swobj in allsws.items():
    s = SwitchDetails(swip, swobj)
    swdetail_list.append(s)
    t = s.set_thread_basic_info()

for sw in swdetail_list:
    status = 'Checking basic info...Please wait.. '
    x.add_row(['', sw.ip, '', '', status])
    sw.t.start()

print(x)
while True:
    exit = True
    utils.print_table_in_same_place(len(swdetail_list), x)
    x.clear_rows()
    for sw in swdetail_list:
        if sw.t.is_alive():
            status = 'Checking basic info...Please wait.. '
            exit = False
            x.add_row(['', sw.ip, '', '', status])
        else:
            status = 'Done checking basic info.'
            x.add_row([sw.name, sw.ip, sw.ver, sw.npv, status])
    time.sleep(0.25)
    if exit:
        utils.print_table_in_same_place(len(swdetail_list), x)
        break

# Clear rows in table
x.clear_rows()
# Start upgrade checks threads
for sw in swdetail_list:
    sw.set_thread_get_upg_img_status(upgver)
    sw.t.start()
    x.add_row([sw.name, sw.ip, sw.ver, sw.npv, sw.retstr])
# Update table, if thread is complete then exit
while True:
    exit = True
    utils.print_table_in_same_place(len(swdetail_list), x)
    x.clear_rows()
    for sw in swdetail_list:
        if sw.t.is_alive():
            exit = False
        if sw.can_upgrade:
            swdetail_upgrade.append(sw)
        x.add_row([sw.name, sw.ip, sw.ver, sw.npv, sw.retstr])
    time.sleep(0.25)
    if exit:
        utils.print_table_in_same_place(len(swdetail_list), x)
        break

swdetail_upgrade.append(sw)
if pc:
    print("Doing checks")
    # dc_obj = Do_Checks(swdetail_upgrade)

log.info("Done with the script..")
END = time.perf_counter()
utils.banner("End of script (Took " + utils.timeelaped(START, END) + " complete)")
