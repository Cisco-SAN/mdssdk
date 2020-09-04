from check_modules import *
from constants import *
import json
import threading
JSON_FILE = 'checks.json'


class Do_Checks(object):
    def __init__(self, swlist_to_upgrade):
        self.swlist_to_upgrade = swlist_to_upgrade
        self.default_checks = []
        self.user_checks = []
        self.check_objects = {}
        self._open_json_file()

        allt = []
        for sw in self.swlist_to_upgrade:
            t = threading.Thread(target=self._create_objects, args=(sw,))
            allt.append(t)
        for t in allt:
            t.start()
        for t in allt:
            t.join()
        print(self.check_objects)
        # self._trigger_get()

    def _open_json_file(self):
        with open(JSON_FILE) as data_file:
            file_dict = json.loads(data_file.read())
        self.default_checks = file_dict[DEFAULT]
        try:
            self.user_checks = file_dict[USER]
        except KeyError:
            self.user_checks = []

        self.all_checks = self.default_checks + self.user_checks
        # print(self.default_checks)
        # print(self.user_checks)

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
        #print(obj)
        return obj
