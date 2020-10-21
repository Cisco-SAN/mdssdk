import unittest

from mdssdk.connection_manager.errors import CLIError
from mdssdk.vsan import Vsan
from tests.test_vsan.vars import *

log = logging.getLogger(__name__)


class TestVsanDelete(unittest.TestCase):
    def __init__(self, testName, sw):
        super().__init__(testName)
        self.switch = sw

    def setUp(self) -> None:
        log.debug(self.switch.version)
        log.debug(self.switch.ipaddr)
        self.vsandb = self.switch.vsans
        while True:
            self.id = get_random_id()
            if self.id not in self.vsandb.keys():
                break
        self.v = Vsan(switch=self.switch, id=self.id)
        self.default_id = 1

    def test_delete(self):
        self.v.create()
        self.assertEqual(self.id, self.v.id)
        self.v.delete()
        self.assertIsNone(self.v.id)

    def test_delete_default_vsan(self):
        i = self.default_id
        v = Vsan(switch=self.switch, id=i)
        with self.assertRaises(CLIError) as e:
            v.delete()
        self.assertEqual(
            'The command " terminal dont-ask ; vsan database ; no vsan '
            + str(i)
            + ' " gave the error " vsan '
            + str(i)
            + ':cannot delete default vsan ".',
            str(e.exception),
        )

    def test_delete_nonexistingvsan(self):
        with self.assertRaises(CLIError) as e:
            self.v.delete()
        self.assertEqual(
            'The command " terminal dont-ask ; vsan database ; no vsan '
            + str(self.id)
            + ' " gave the error " vsan '
            + str(self.id)
            + ':vsan not configured ".',
            str(e.exception),
        )

    def tearDown(self) -> None:
        if self.v.id is not None:
            self.v.delete()
        self.assertEqual(self.vsandb.keys(), self.switch.vsans.keys())
