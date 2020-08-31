from .check import Check


class Check_Interface(Check):
    def __init__(self, sw):
        super().__init__(sw)
        self.name = "INTERFACE"
        self.cmd_list = ["show interface brief"]

    def compare(self):
        pass
