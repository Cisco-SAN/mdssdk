import unittest


class TestSwitchShowList(unittest.TestCase):

    def test_show_list(self):
        print("Output of show list : " + str(self.commands))
        print(self.switch.show_list(self.commands))

    def test_show_rawtext(self):
        print("Output of show list(raw text) : " + str(self.commands))
        print(self.switch.show_list(self.commands, True))
