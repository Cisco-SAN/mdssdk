import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.devicealias import DeviceAlias
from tests.test_device_alias.vars import *

log = logging.getLogger(__name__)


class TestDeviceAliasCreate(unittest.TestCase):
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

    def test_create(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])
        self.d.delete(self.name)
        newdb = self.d.database
        if newdb is not None:
            self.assertNotIn(self.name, newdb.keys())
            self.assertNotIn(self.pwwn, newdb.values())

    def test_create_name_invalid(self):
        invalid_name = {
            "da1&": get_random_pwwn()
        }  # da name a-zA-Z1-9 - _ $ ^    64chars max
        name = list(invalid_name.keys())[0]
        pwwn = list(invalid_name.values())[0]
        with self.assertRaises(CLIError) as e:
            self.d.create(invalid_name)
        self.assertEqual(
            'The command " device-alias database ;  device-alias name '
            + str(name)
            + " pwwn "
            + str(pwwn)
            + ' ; " gave the error " Illegal character present in the name ".',
            str(e.exception),
        )
        self.d.clear_lock()

    def test_create_name_invalidfirstchar(self):
        invalidfirstchar = {"1da": "53:66:61:01:0e:00:01:ff"}
        name = list(invalidfirstchar.keys())[0]
        pwwn = list(invalidfirstchar.values())[0]
        with self.assertRaises(CLIError) as e:
            self.d.create(invalidfirstchar)
        self.assertEqual(
            'The command " device-alias database ;  device-alias name '
            + str(name)
            + " pwwn "
            + str(pwwn)
            + ' ; " gave the error " Illegal first character. Name must start with a letter ".',
            str(e.exception),
        )
        self.d.clear_lock()

    def test_create_name_beyondmax(self):
        beyondmax = {
            "da123456789123456789123456789123456789123456789123456789123456789": get_random_pwwn()
        }
        name = list(beyondmax.keys())[0]
        pwwn = list(beyondmax.values())[0]
        with self.assertRaises(CLIError) as e:
            self.d.create(beyondmax)
        self.assertEqual(
            'The command " device-alias database ;  device-alias name '
            + str(name)
            + " pwwn "
            + str(pwwn)
            + ' ; " gave the error " % String exceeded max length of (64) ".',
            str(e.exception),
        )

    def test_create_pwwn_existing(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        newname = get_random_string()
        with self.assertRaises(CLIError) as e:
            self.d.create({newname: self.pwwn})
        self.assertIn(
            "Another device-alias already present with the same pwwn", str(e.exception)
        )

        # DB should not be updated with the new name
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        self.d.delete(self.name)

    def test_create_name_existing(self):
        self.d.create({self.name: self.pwwn})
        newdb = self.d.database
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        newpwwn = get_random_pwwn()
        with self.assertRaises(CLIError) as e:
            self.d.create({self.name: newpwwn})
        self.assertIn("Device Alias already present", str(e.exception))

        # DB should not be updated with the new pwwn
        self.assertIn(self.name, newdb.keys())
        self.assertEqual(self.pwwn, newdb[self.name])

        self.d.delete(self.name)

    def tearDown(self) -> None:
        try:
            self.d.delete(self.name)
        except CLIError as c:
            if "Device Alias not present" not in c.message:
                self.fail("Tear down failed: " + c.message)
        enddb = self.d.database
        if enddb is not None:
            self.assertEqual(enddb, self.olddb)
