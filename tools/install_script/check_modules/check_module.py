from .check import Check


class Check_Module(Check):
    def __init__(self, sw):
        super().__init__(sw)
        self.name = "MODULE"
        self.cmd_list = ["show module"]

    def compare(self):
        pass
