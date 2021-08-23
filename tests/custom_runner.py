import csv
import unittest

import time

writer = csv.writer(open("time.csv", "w", newline=""))


class MyTestLoader(unittest.TestLoader):
    def __init__(self, arg):
        super().__init__()
        self.arg = arg

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all test cases contained in testCaseClass"""
        if issubclass(testCaseClass, unittest.suite.TestSuite):
            raise TypeError(
                "Test cases should not be derived from "
                "TestSuite. Maybe you meant to derive from "
                "TestCase?"
            )
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if not testCaseNames and hasattr(testCaseClass, "runTest"):
            testCaseNames = ["runTest"]

        # Modification here: parse keyword arguments to testCaseClass.
        test_cases = []
        for test_case_name in testCaseNames:
            test_cases.append(testCaseClass(test_case_name, self.arg))

        loaded_suite = self.suiteClass(test_cases)
        return loaded_suite


class TimeLoggingTestResult(unittest.TextTestResult):
    def startTest(self, test):
        self._started_at = time.time()
        super().startTest(test)

    def addSuccess(self, test):
        elapsed = time.time() - self._started_at
        writer.writerow([self.getDescription(test), "pass", "{:.03}s ".format(elapsed)])
        self.stream.write("{:.03}s ".format(elapsed))
        super().addSuccess(test)

    def addError(self, test, err):
        writer.writerow([self.getDescription(test), "error", 0])
        super().addError(test, err)

    def addFailure(self, test, err):
        writer.writerow([self.getDescription(test), "fail", 0])
        super().addFailure(test, err)

    def addSkip(self, test, reason):
        writer.writerow([self.getDescription(test), "skipped: " + str(reason), 0])
        super().addSkip(test, reason)
