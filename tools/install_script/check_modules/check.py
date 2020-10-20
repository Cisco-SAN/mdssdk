import logging

log = logging.getLogger(__name__)


class Check(object):
    def __init__(self, sw):
        self.name = "check"
        self.sw = sw
        self.only_npiv = False
        self.only_npv = False
        self.check_pass = False
        self.cmd_list = []
        self.result = {}
        self.before_data = {}
        self.after_data = {}
        self.diff_ba_data = {}
        self.diff_ab_data = {}

    def run_cmd(self, before=True):
        for cmd in self.cmd_list:
            out = self.sw.get_cmd_output(cmd, only_npv=self.only_npv, only_npiv=self.only_npiv)
            if before:
                self.before_data[cmd] = out.split("\n")
            else:
                self.after_data[cmd] = out.split("\n")
            log.debug("run_cmd-" + self.name)
            log.debug(self.before_data)
            log.debug(self.after_data)

    def compare(self):
        log.debug("compare start" + self.name)
        log.debug(self.before_data)
        log.debug(self.after_data)
        for cmd in self.cmd_list:
            before_set = set(self.before_data[cmd])
            after_set = set(self.after_data[cmd])
            # Get elements which are present in first_list but not in sec_list
            diff1 = set(before_set) - set(after_set)
            self.diff_ba_data[cmd] = list(diff1)
            diff1 = set(after_set) - set(before_set)
            self.diff_ab_data[cmd] = list(diff1)
            log.debug("compare" + self.name)
            log.debug(self.diff_ba_data)
            log.debug(self.diff_ab_data)

    def collect_data(self):
        log.debug("collect_data start" + self.name)
        for cmd in self.cmd_list:
            self.result[cmd] = {}
            self.result[cmd]['BEFORE'] = self.before_data[cmd]
            self.result[cmd]['AFTER'] = self.after_data[cmd]
            self.result[cmd]['DIFF_BA'] = self.diff_ba_data[cmd]
            self.result[cmd]['DIFF_AB'] = self.diff_ab_data[cmd]
        log.debug("collect_data end" + self.name)
        log.debug(self.result)
