import csv
import json
import logging
import time
import unittest

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)
logFormatter = logging.Formatter(
    "[%(asctime)s] [%(module)-14.14s] [%(levelname)-5.5s] %(message)s"
)
# Add stdout handler, with level INFO
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logFormatter)
# logging.getLogger().addHandler(console)

# Add file rotating handler, with level DEBUG
fileHandler = logging.FileHandler("test.log")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(logFormatter)
logging.getLogger().addHandler(fileHandler)

log = logging.getLogger(__name__)

log.info("Starting all tests...")

writer = csv.writer(open('time.csv', 'w', newline=''))

class TimeLoggingTestResult(unittest.TextTestResult):

    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        writer.writerow([self.getDescription(test), "pass", elapsed])
        self.stream.write("{:.03}s ".format(elapsed))
        super().addSuccess(test)

    def addError(self, test, err):
        writer.writerow([self.getDescription(test), "error", 0])
        super().addError(test, err)

    def addFailure(self, test, err):
        writer.writerow([self.getDescription(test), "fail", 0])
        super().addFailure(test, err)
 
def get_suite_list():
    suiteList = []
    suiteList.append(
        unittest.TestLoader().discover("tests.test_device_alias", "test_*.py")
    )
    suiteList.append(unittest.TestLoader().discover("tests.test_fc", "test_*.py"))
    suiteList.append(
        unittest.TestLoader().discover("tests.test_port_channel", "test_*.py")
    )
    suiteList.append(unittest.TestLoader().discover('tests.test_fcns', 'test_*.py'))
    suiteList.append(unittest.TestLoader().discover('tests.test_flogi', 'test_*.py'))
    suiteList.append(unittest.TestLoader().discover("tests.test_switch", "test_*.py"))
    suiteList.append(unittest.TestLoader().discover("tests.test_vsan", "test_*.py"))
    suiteList.append(unittest.TestLoader().discover("tests.test_zone", "test_*.py"))
    suiteList.append(
        unittest.TestLoader().discover("tests.test_zoneset", "test_zoneset*.py")
    )
    return suiteList


for conntype in ["ssh", "https"]:
    with open("switch_details.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["connection_type"] = conntype  # <--- add value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

        print("\nRunning tests on '" + data['ip_address'] + "' with connection type '" + conntype + "'")
        writer.writerow([conntype])
        print(
            "\nRunning tests on '"
            + data["ip_address"]
            + "' with connection type '"
            + conntype
            + "'"
        )
        comboSuite = unittest.TestSuite(get_suite_list())
        unittest.TextTestRunner(verbosity=2, failfast=True, resultclass=TimeLoggingTestResult).run(comboSuite)
        time.sleep(0.01)
