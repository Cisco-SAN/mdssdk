# 13cmx18cm
# 5.11811x7.08661
# 15.5cmx20.5cm
# 6.102362x8.070866


from mdssdk.fabric import Fabric
from mdssdk.switch import Switch
from prettytable import PrettyTable
import tools.install_script.utils as utils
from tools.install_script.switch_details import SwitchDetails
from tools.install_script.do_checks import Do_Checks

import sys
from datetime import datetime
import threading
import multiprocessing
from concurrent.futures.thread import ThreadPoolExecutor
import logging
import time

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)
logFileFormatter = logging.Formatter(
    "[%(asctime)s] [%(module)-14.14s] [%(lineno)d] [%(levelname)-5.5s] %(message)s"
)
logConsoleFormatter = logging.Formatter(
    "[%(asctime)s] %(message)s"
)
# Add stdout handler, with level INFO
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logConsoleFormatter)
logging.getLogger('mdssdk').addHandler(console)
logging.getLogger('install').addHandler(console)

# Add file handler, with level DEBUG
fileHandler = logging.FileHandler("install_script.log", mode='w')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFileFormatter)
logging.getLogger('mdssdk').addHandler(fileHandler)
logging.getLogger('install').addHandler(fileHandler)

log = logging.getLogger('install')


# print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
# sw = Switch("10.126.94.129", "admin", "nbv!2345", connection_type='ssh',verify_ssl = False)
# print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
# sys.exit()


def main():
    sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=40, cols=150))

    y = PrettyTable(title="All Upgradable Switches")
    y.field_names = ["Switch Name", "IP Address", "Version", "Upgrade Version", "Install Status", "Time Elapsed"]
    y.sortby = "IP Address"
    x = PrettyTable(title="All Switches in the fabric")
    x.field_names = ["Switch Name", "IP Address", "Version", "NPV?", "Status", "Time Elapsed"]
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
        s = Switch(swip, uname, pw, connection_type='ssh', timeout=600)
    except Exception as e:
        print("ERROR!! Could not connect to the seed switch via ssh. Please check the connection.")
        log.exception(e)
        exit()

    if s.npv:
        msg = "ERROR!! Cannot discover fabric using NPV switch. Please give an NPIV address"
        print(msg)
        log.debug(msg)
        exit()

    f1 = Fabric(swip, uname, pw, connection_type='ssh', timeout=600)
    f1.all_switches_in_fabric(discover_npv=npv_req)

    ############ START OF BASIC INFO ############################
    allsws = f1.switches
    swdetail_list = []
    swdetail_upgrade = []
    for swip, swobj in allsws.items():
        s = SwitchDetails(swip, swobj)
        swdetail_list.append(s)
        s.set_thread_basic_info()

    for sw in swdetail_list:
        status = 'Checking basic info...Please wait.. '
        x.add_row(['', sw.ip, '', '', status, ''])

    print(x)
    while True:
        exit = True
        utils.print_table_in_same_place(len(swdetail_list), x)
        x.clear_rows()
        for sw in swdetail_list:
            if sw.t.is_alive():
                status = utils.BLUE('Checking basic info...Please wait.. ')
                exit = False
                x.add_row(['', sw.ip, '', '', status, sw.elapsed_time])
            else:
                status = utils.GREEN('Done checking basic info.')
                x.add_row([sw.name, sw.ip, sw.ver, sw.npv, status, sw.elapsed_time])
        time.sleep(0.25)
        if exit:
            utils.print_table_in_same_place(len(swdetail_list), x)
            break
    ############ END OF BASIC INFO ############################

    ############ START OF UPG IMAGE STATUS  ############################
    # Clear rows in table
    x.clear_rows()
    # Start upgrade checks threads
    for sw in swdetail_list:
        try:
            sw.set_thread_get_upg_img_status(upgver)  # TODO collect imact check info and store
        except Exception as e:
            log.error(e)
        x.add_row([sw.name, sw.ip, sw.ver, sw.npv, sw.retstr, sw.elapsed_time])
    utils.print_table_in_same_place(len(swdetail_list), x)
    x.clear_rows()
    # Update table, if thread is complete then exit
    while True:
        exit = True
        for sw in swdetail_list:
            if sw.t.is_alive():
                exit = False
            x.add_row([sw.name, sw.ip, sw.ver, sw.npv, sw.retstr, sw.elapsed_time])
        time.sleep(0.25)
        utils.print_table_in_same_place(len(swdetail_list), x)
        x.clear_rows()
        if exit:
            break

    for sw in swdetail_list:
        if sw.can_upgrade:
            swdetail_upgrade.append(sw)
    if not swdetail_upgrade:
        log.info("!!!!!!   No switches to upgrade   !!!!!!")
        log.info("Done with the script!")
        return

    ############ END OF UPG IMAGE STATUS  ############################

    ############ START OF PRE CHECK  ############################
    if pc:
        log.info("Collecting data from all switches BEFORE upgrade")
        dc_obj = Do_Checks(swdetail_upgrade)
    ############ END OF PRE CHECK  ############################

    ############ START OF ISSU/D ############################
    # Now start the upgrade
    # Clear rows in table
    x = y
    x.clear_rows()
    # Start upgrade checks threads
    for sw in swdetail_upgrade:
        try:
            sw.set_thread_to_start_upgrade()  # TODO: pass timeout if required
        except Exception as e:
            log.debug(e, exc_info=True)
        x.add_row([sw.name, sw.ip, sw.ver, upgver, utils.BLUE("Starting Install.."), sw.elapsed_time])
    print(x)
    while True:
        exit = True
        utils.print_table_in_same_place(len(swdetail_upgrade), x)
        x.clear_rows()
        for sw in swdetail_upgrade:
            if sw.t.is_alive():
                exit = False
            x.add_row([sw.name, sw.ip, sw.ver, upgver, sw.install_status, sw.elapsed_time])
            time.sleep(0.25)
        if exit:
            utils.print_table_in_same_place(len(swdetail_upgrade), x)
            break
    ############ END OF ISSU/D ############################

    if pc:
        log.info("Collecting data from all switches AFTER upgrade")
        dc_obj._reconnect_swobjs()
        dc_obj._after()


if __name__ == '__main__':
    utils.banner("Starting install script for the entire fabric")
    START = time.perf_counter()
    main()
    END = time.perf_counter()
    utils.banner("End of script (Took " + utils.timeelaped(START, END) + " complete)")
    sys.exit()
