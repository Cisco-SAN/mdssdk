from .check import Check


class Check_CFS(Check):
    # IF Check_CFS lock is present in the switch we declare it as failure
    def __init__(self, sw):
        super().__init__(sw)
        self.name = "CFS"
        self.cmd_list = ["show cfs lock"]
        self.run_cmd()
