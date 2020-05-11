import unittest

from mdssdk.connection_manager.errors import CLIError


class TestSwitchConfigList(unittest.TestCase):

    def test_config_list(self):
        print("Result of config list : " + str(self.commands))
        print(self.switch.config_list(self.commands))

    def test_config_list_error(self):
        with self.assertRaises(CLIError) as e:
            self.switch.config_list(self.commands_clierror)
        print("Config list : " + str(self.commands_clierror) + " raises " + str(e.exception))
