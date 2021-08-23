__author__ = "Suhas Bharadwaj (subharad)"

import re


class ShowProcessAcltcamFwdEngInput(object):
    def __init__(self, output):
        self.__alloutput = output
        self.__pat_for_tcam_entry = "^([0-9a-f]+)\s+.*"

        self.__data = []

        self.__process_output()

    def __process_output(self):
        for line in self.__alloutput:
            matchObj = re.match(self.__pat_for_tcam_entry, line.strip(" "))
            if matchObj:
                # print line
                loc = matchObj.group(1)
                self.__data.append([loc])

    def get_all_data(self):
        return tuple(self.__data)

    def get_all_location_details(self):
        return tuple([(s[0]) for s in self.__data])
