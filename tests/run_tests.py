import json
import logging
import unittest

import time

from custom_runner import MyTestLoader, TimeLoggingTestResult
from mdssdk.switch import Switch

START = time.perf_counter()

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)
logFormatter = logging.Formatter(
    "[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s"
)

logging.getLogger("paramiko").setLevel(logging.WARNING)
logging.getLogger("netmiko").setLevel(logging.WARNING)
# Add stdout handler, with level INFO
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logFormatter)
logging.getLogger(__name__).addHandler(console)

# Add file handler, with level DEBUG
fileHandler = logging.FileHandler("test.log", mode="w")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logging.getLogger("mdssdk").addHandler(fileHandler)
logging.getLogger(__name__).addHandler(fileHandler)

log = logging.getLogger(__name__)

log.info("Starting all tests...")


def get_suite_list(sw):
    suiteList = []
    suiteList.append(MyTestLoader(sw).discover("test_fc", "test_*.py"))
    suiteList.append(MyTestLoader(sw).discover("test_port_channel", "test_*.py"))
    suiteList.append(MyTestLoader(sw).discover("test_switch", "test_*.py"))
    suiteList.append(MyTestLoader(sw).discover("test_vsan", "test_*.py"))
    if not sw.npv:
        suiteList.append(MyTestLoader(sw).discover("test_device_alias", "test_*.py"))
        suiteList.append(MyTestLoader(sw).discover("test_fcns", "test_*.py"))
        suiteList.append(MyTestLoader(sw).discover("test_flogi", "test_*.py"))
        suiteList.append(MyTestLoader(sw).discover("test_zone", "test_*.py"))
        suiteList.append(MyTestLoader(sw).discover("test_zoneset", "test_*.py"))
    return suiteList


for conntype in ["https"]:
    with open("switch_details.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        print(
            "\nRunning tests on '"
            + data["ip_address"]
            + "' with connection type '"
            + conntype
            + "'"
        )
        log.info("Creating switch object")
        sw = Switch(
            ip_address=data["ip_address"],
            username=data["username"],
            password=data["password"],
            connection_type=conntype,
            port=data["port"],
            timeout=data["timeout"],
            verify_ssl=False,
        )
        log.info("Connection type for switch object is " + sw.connection_type)
        comboSuite = unittest.TestSuite(get_suite_list(sw))
        unittest.TextTestRunner(
            verbosity=2, failfast=True, resultclass=TimeLoggingTestResult
        ).run(comboSuite)
        time.sleep(0.01)

END = time.perf_counter()
hours, rem = divmod(END - START, 3600)
minutes, seconds = divmod(rem, 60)
log.info(
    "End of Tests (Took "
    + ("{:0>1}h:{:0>1}m:{:02.1f}s".format(int(hours), int(minutes), seconds))
    + " to complete)"
)
