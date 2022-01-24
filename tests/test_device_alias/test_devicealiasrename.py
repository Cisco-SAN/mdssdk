import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasRename(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.d = DeviceAlias(self.switch)
        self.olddb = self.d.database
        if self.olddb is None:
            self.name = get_random_string()
            self.pwwn = get_random_pwwn()
        else:
            while True:
                self.name = get_random_string()
                self.pwwn = get_random_pwwn()
                if (
                        self.name not in self.olddb.keys()
                        and self.pwwn not in self.olddb.values()
                ):
                    break
        log.debug({self.name: self.pwwn})

    def test_rename(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])
        while True:
            self.newname_to_replace = get_random_string()
            if self.newname_to_replace not in newdb.keys():
                break
        self.d.rename(oldname=self.name, newname=self.newname_to_replace)
        chkdb = self.d.database
        self.assertIn(self.newname_to_replace, chkdb.keys())
        self.assertEqual(self.pwwn, chkdb[self.newname_to_replace])
        self.assertNotIn(self.name, chkdb.keys())
        self.d.delete(self.newname_to_replace)
        chkdb = self.d.database
        if chkdb is not None:
            self.assertNotIn(self.newname_to_replace, chkdb.keys())
            self.assertNotIn(self.pwwn, chkdb.values())
            self.assertNotIn(self.name, chkdb.keys())

    def test_rename_not_present(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])
        while True:
            self.newname_to_replace = get_random_string()
            if self.newname_to_replace not in newdb.keys():
                break
        with self.assertRaises(CLIError) as e:
            self.d.rename(oldname=self.newname_to_replace, newname=self.name)
        self.assertIn("Device Alias not present", str(e.exception))

        self.d.delete(self.name)
        chkdb = self.d.database
        if chkdb is not None:
            self.assertNotIn(self.newname_to_replace, chkdb.keys())
            self.assertNotIn(self.pwwn, chkdb.values())
            self.assertNotIn(self.name, chkdb.keys())

    def test_rename_already_present(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        with self.assertRaises(CLIError) as e:
            self.d.rename(oldname=self.name, newname=self.name)
        self.assertIn(
            "Target device-alias name already in use. Please specify a new name.",
            str(e.exception),
        )

        self.d.delete(self.name)
        chkdb = self.d.database
        if chkdb is not None:
            self.assertNotIn(self.pwwn, chkdb.values())
            self.assertNotIn(self.name, chkdb.keys())

    def test_rename_invalid(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        invalid_name = "da1&"  # da name a-zA-Z1-9 - _ $ ^    64chars max
        with self.assertRaises(CLIError) as e:
            self.d.rename(oldname=self.name, newname=invalid_name)
        self.assertIn("Illegal character present in the name", str(e.exception))
        self.d.clear_lock()

        self.d.delete(self.name)
        chkdb = self.d.database
        if chkdb is not None:
            self.assertNotIn(self.pwwn, chkdb.values())
            self.assertNotIn(self.name, chkdb.keys())

    def tearDown(self) -> None:
        try:
            self.d.delete(self.name)
        except CLIError as c:
            if "Device Alias not present" not in c.message:
                self.fail("Tear down failed: " + c.message)
        enddb = self.d.database
        if enddb is not None:
            self.assertEqual(enddb, self.olddb)
