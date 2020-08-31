from .check import Check


class Check_CFS(Check):
    # IF Check_CFS lock is present in the switch we declare it as failure
    def __init__(self, sw):
        super().__init__(sw)
        self.name = "CFS"
        self.cmd_list = ["show cfs lock"]

    def compare(self):
        pass

    # >> > s = ['a', 'b', 'c']
    # >> > f = ['a', 'b', 'd', 'c']
    # >> > ss = set(s)
    # >> > fs = set(f)
    # >> > print
    # ss.intersection(fs)
    # ** set(['a', 'c', 'b']) **
    #
    # >> > print
    # ss.union(fs)
    # ** set(['a', 'c', 'b', 'd']) **
    # >> > print
    # ss.union(fs) - ss.intersection(fs)
    # ** set(['d']) **
