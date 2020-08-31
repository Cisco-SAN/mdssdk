from check_modules import *
from constants import *
import json

JSON_FILE = 'checks.json'


class Do_Checks(object):
    def __init__(self, swlist_to_upgrade):
        self.swlist_to_upgrade = swlist_to_upgrade
        # print("swlist_to_upgrade")
        # for sw in self.swlist_to_upgrade:
        #    print(sw.ip)
        self.default_checks = ''
        self.user_checks = ''
        self.check_objects = {}
        self._open_json_file()
        self._create_objects()
        self._trigger_get()

    def _open_json_file(self):
        with open(JSON_FILE) as data_file:
            file_dict = json.loads(data_file.read())
        self.default_checks = file_dict[DEFAULT]
        self.user_checks = file_dict[USER]
        print(self.default_checks)
        print(self.user_checks)

    def _create_objects(self):
        for sw in self.swlist_to_upgrade:
            tmp_list = []
            for each_def_chk in self.default_checks:
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
        print(obj)
        return obj
