from tools.install_script.check_modules import check_cfs, check_module, check_interface, check_flogi
from tools.install_script.constants import *
import pprint
import json
import threading
from collections import OrderedDict
import collections
import xlsxwriter
import logging

log = logging.getLogger(__name__)

JSON_FILE = 'checks.json'


class Do_Checks(object):
    def __init__(self, swlist_to_upgrade):
        self.swlist_to_upgrade = swlist_to_upgrade
        self.default_checks = []
        self.user_checks = []
        self.check_objects = {}
        self._open_json_file()
        self.write_data_list = []
        self._before()

    def _reconnect_swobjs(self):
        for sw in self.swlist_to_upgrade:
            sw.swobj._reconnect_to_ssh()
            log.debug("do_checks")
            log.debug(sw.swobj.version)

    def _before(self):
        allt = []
        for sw in self.swlist_to_upgrade:
            t = threading.Thread(target=self._create_objects, args=(sw,))
            allt.append(t)
        for t in allt:
            t.start()
        for t in allt:
            t.join()

    def _after(self):
        allt = []
        for sw, objlist in self.check_objects.items():
            t = threading.Thread(target=self._after_issu, args=(sw, objlist,))
            allt.append(t)
        for t in allt:
            t.start()
        for t in allt:
            t.join()
        self.print_it()

    def _after_issu(self, sw, objlist):
        write_data = {}
        for each_check_obj in objlist:
            log.debug(" run_cmd after issu")
            each_check_obj.run_cmd(before=False)
            log.debug(" compare")
            each_check_obj.compare()
            log.debug(" collect data")
            each_check_obj.collect_data()
        write_data['IP'] = sw.ip
        write_data['PREV VER'] = sw.ver
        write_data['CURR VER'] = sw.swobj.version
        for each_check_obj in objlist:
            write_data[each_check_obj.name] = each_check_obj.result
        self.write_data_list.append(write_data)

    def _open_json_file(self):
        with open(JSON_FILE) as data_file:
            file_dict = json.loads(data_file.read())
        self.default_checks = file_dict[DEFAULT]
        try:
            self.user_checks = file_dict[USER]
        except KeyError:
            self.user_checks = []

        self.all_checks = self.default_checks + self.user_checks

    def _create_objects(self, sw):
        tmp_list = []
        for each_def_chk in self.all_checks:
            z = self._get_check_object(sw, each_def_chk)
            if z is not None:
                tmp_list.append(z)
        if tmp_list:
            self.check_objects[sw] = tmp_list

    def _get_check_object(self, sw, check_component):
        obj = None
        # print(check_component)
        if CFS == check_component:
            obj = check_cfs.Check_CFS(sw)
        if MODULE == check_component:
            obj = check_module.Check_Module(sw)
        if INTERFACE == check_component:
            obj = check_interface.Check_Interface(sw)
        if FLOGI == check_component:
            obj = check_flogi.Check_Flogi(sw)
        # print(obj)
        return obj

    def _json_to_excel(self, ws, data, row=0, col=0):
        if isinstance(data, list):
            row -= 1
            for value in data:
                row = self._json_to_excel(ws, value, row + 1, col)
        elif isinstance(data, dict):
            max_row = row
            start_row = row
            for key, value in data.items():
                row = start_row
                ws.write(row, col, key)
                row = self._json_to_excel(ws, value, row + 1, col)
                max_row = max(max_row, row)
                col += 1
            row = max_row
        else:
            ws.write(row, col, data)

        return row

    def write_to_excel(self):
        # pprint.pprint(self.write_data_list)
        self.print_it()

    def print_it(self):
        # Ip
        # B_VER
        # A_VER
        # CMD_B-A
        # CMD_A-B

        mylist = []
        for eachelem in self.write_data_list:
            temp_dict = OrderedDict()
            for k, v in eachelem.items():
                if "IP" in k:
                    temp_dict["IP"] = v
                elif 'CURR VER' in k:
                    temp_dict["CURR_VER"] = v
                elif 'PREV VER' in k:
                    temp_dict["PREV_VER"] = v
                else:
                    for cmd, details in v.items():
                        temp_dict[cmd + "_B-A"] = details['DIFF_BA']
                        temp_dict[cmd + "_A-B"] = details['DIFF_AB']
            if temp_dict:
                od = collections.OrderedDict(sorted(temp_dict.items()))
            mylist.append(od)
        # pprint.pprint(mylist)
        log.info("Writing to excel. Please wait...")
        jsondata = json.dumps(mylist)
        data = json.loads(jsondata, object_pairs_hook=OrderedDict)
        wb = xlsxwriter.Workbook("output.xlsx")
        ws = wb.add_worksheet()
        self._json_to_excel(ws, data)
        wb.close()
