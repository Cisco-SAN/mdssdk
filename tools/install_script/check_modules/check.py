# from intall_script.constants import *
from .utility import *


class Check(object):
    def __init__(self, sw):
        self.sw = sw
        self.check_pass = False
        self.cmd_list = []
        self.before_data = {}
        self.after_data = {}
        self.diff_data = {}
        self.run_cmd()

    def run_cmd(self, before=True):
        for cmd in self.cmd_list:
            out = self.sw.get_cmd_output(cmd)
            if before:
                self.before_data[cmd] = out
            else:
                self.after_data[cmd] = out
