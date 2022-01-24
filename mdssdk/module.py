import logging

import time

from .nxapikeys import modulekeys
from .utility.utils import get_key
from .connection_manager.errors import UnsupportedSwitch
from .constants import VALID_PIDS_MDS

log = logging.getLogger(__name__)


class Module(object):
    """
    Switch's module class

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
        >>> mod_handler = switch_obj.modules
        >>> print(mod_handler)
        [{1: <mdslib.module.Module object at 0x10ad710d0>}, {2: <mdslib.module.Module object at 0x10ad71190>},
        {3: <mdslib.module.Module object at 0x10ad711d0>}, {4: <mdslib.module.Module object at 0x10ad71050>},
        {5: <mdslib.module.Module object at 0x10abdf190>}]

    """

    def __init__(self, switch, mod_num, modinfo):
        self.__swobj = switch
        self.__modinfo = modinfo
        self._SW_VER = switch._SW_VER
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

        self.__mod_num = mod_num
        if self.__swobj.is_connection_type_ssh():
            self.__mod_ports = self.__modinfo["ports"]
            self.__mod_modtype = self.__modinfo["type"]
            self.__mod_model = self.__modinfo["model"]
            self.__mod_status = self.__modinfo["status"]
        else:
            self.__mod_ports = self.__modinfo[
                get_key(modulekeys.MOD_PORTS, self._SW_VER)
            ]
            self.__mod_modtype = self.__modinfo[
                get_key(modulekeys.MOD_TYPE, self._SW_VER)
            ]
            self.__mod_model = self.__modinfo[
                get_key(modulekeys.MOD_MODEL, self._SW_VER)
            ]
            self.__mod_status = self.__modinfo[
                get_key(modulekeys.MOD_STATUS, self._SW_VER)
            ]

    @property
    def module_number(self):
        """
        Get module number

        :return: module number
        :rtype: int
        :example:
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
            >>> mod_handler = list(switch_obj.modules.values())
            >>> first_mod_handler = mod_handler[0]
            >>> print(first_mod_handler.module_number)
            2
            >>>

        """

        if self.__swobj.is_connection_type_ssh():
            self.__mod_num = self.__modinfo["module"]
        else:
            self.__mod_num = self.__modinfo[get_key(modulekeys.MOD_NUM, self._SW_VER)]
        return int(self.__mod_num)

    @property
    def ports(self):
        """
        Get number of ports on the module

        :return: number of ports on the module
        :rtype: int
        :example:
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
            >>> mod_handler = list(switch_obj.modules.values())
            >>> first_mod_handler = mod_handler[0]
            >>> print(first_mod_handler.ports)
            48
            >>>
        """

        if self.__mod_ports is None:
            self.__modinfo = self.__get_modinfo()
        if self.__swobj.is_connection_type_ssh():
            self.__mod_ports = self.__modinfo["ports"]
        else:
            self.__mod_ports = self.__modinfo[
                get_key(modulekeys.MOD_PORTS, self._SW_VER)
            ]
        return int(self.__mod_ports)

    @property
    def type(self):
        """
        Get type of the module

        :return: type of the module
        :rtype: str
        :example:
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
            >>> mod_handler = list(switch_obj.modules.values())
            >>> first_mod_handler = mod_handler[0]
            >>> print(first_mod_handler.type)
            2/4/8/10/16 Gbps Advanced FC Module
            >>>
        """
        if self.__mod_modtype is None:
            self.__modinfo = self.__get_modinfo()
        if self.__swobj.is_connection_type_ssh():
            self.__mod_modtype = self.__modinfo["type"]
        else:
            self.__mod_modtype = self.__modinfo[
                get_key(modulekeys.MOD_TYPE, self._SW_VER)
            ]
        return self.__mod_modtype

    @property
    def model(self):
        """
        Get model of the module

        :return: model of the module
        :rtype: str
        :example:
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
            >>> mod_handler = list(switch_obj.modules.values())
            >>> first_mod_handler = mod_handler[0]
            >>> print(first_mod_handler.model)
            DS-X9448-768K9
            >>>
        """
        if self.__mod_model is None:
            self.__modinfo = self.__get_modinfo()
        if self.__swobj.is_connection_type_ssh():
            self.__mod_model = self.__modinfo["model"]
        else:
            self.__mod_model = self.__modinfo[
                get_key(modulekeys.MOD_MODEL, self._SW_VER)
            ]
        return self.__mod_model

    @property
    def status(self):
        """
        Get status of the module

        :return: status of the module
        :rtype: str
        :example:
            >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
            >>> mod_handler = list(switch_obj.modules.values())
            >>> first_mod_handler = mod_handler[0]
            >>> print(first_mod_handler.status)
            ok
            >>>
        """
        self.__modinfo = self.__get_modinfo()
        if self.__swobj.is_connection_type_ssh():
            # print(self.__modinfo)
            self.__mod_status = self.__modinfo["status"]
        else:
            self.__mod_status = self.__modinfo[
                get_key(modulekeys.MOD_STATUS, self._SW_VER)
            ]
        return self.__mod_status

    # TODO
    # def reload(self, non_disruptive=False):
    #     pass

    def __get_modinfo(self):
        cmd = "show module " + str(self.__mod_num)
        out = self.__swobj.show(cmd)
        if self.__swobj.is_connection_type_ssh():
            retout = out[0]
            if "Ejector status could not be retrieved" in retout:
                time.sleep(5)
                cmd = "show module " + str(self.__mod_num)
                out = self.__swobj.show(cmd)
                retout = out[0]
        else:
            retout = out["TABLE_modinfo"]["ROW_modinfo"]
            if type(retout) is list:
                retout = retout[0]
        return retout
