import unittest

from mdssdk.connection_manager.errors import CLIError


class TestSwitchConfig(unittest.TestCase):

    def test_config(self):
        print("Result of config : " + str(self.commands))
        print(self.switch.config(self.commands))

    def test_config_error(self):
        with self.assertRaises(CLIError) as e:
            self.switch.config(self.commands_clierror)
        print("Config : " + str(self.commands_clierror) + " raises " + str(e.exception))
