import unittest


class TestSwitchShow(unittest.TestCase):

    def test_show(self):
        print("Output of show : " + str(self.commands))
        print(self.switch.show(self.commands))

    def test_show_rawtext(self):
        print("Output of show(raw text) : " + str(self.commands))
        print(self.switch.show(self.commands, True))
