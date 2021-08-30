import logging
import re

from .connection_manager.errors import CLIError, UnsupportedSwitch
from .constants import VALID_PIDS_MDS

log = logging.getLogger(__name__)


class Flogi(object):
    def __init__(self, switch):
        self.__swobj = switch
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

    def database(self, vsan=None, interface=None, fcid=None):
        """
        Get flogi database

        :param vsan: id of vsan (optional parameter, defaults to None)
        :type vsan: int or None
        :param interface: interface name (optional parameter, defaults to None)
        :type interface: str or None
        :param fcid: fcid (optional parameter, defaults to None)
        :type fcid: str or None
        :return: flogi database
        :rtype: list
        :example:
            >>> flogi_obj = Flogi(switch_obj)
            >>> print(flogi_obj.database())
             [{'interface': 'fc1/17', 'vsan': 1, 'fcid': '0x2c0020', 'port_name': '10:00:54:7f:ee:eb:2c:25', 'node_name': '20:05:00:11:0d:fd:5f:00'},
             {'interface': 'fc1/17', 'vsan': 1, 'fcid': '0x2c0021', 'port_name': '10:00:54:7f:ee:eb:2d:25', 'node_name': '20:05:00:11:0d:fd:5f:00'},
             {'interface': 'sup-fc0', 'vsan': 13, 'fcid': '0x220000', 'port_name': '10:00:00:de:fb:b1:86:a1', 'node_name': '20:00:00:de:fb:b1:86:a0'},
             {'interface': 'sup-fc0', 'vsan': 14, 'fcid': '0x200000', 'port_name': '10:00:00:de:fb:b1:86:a1', 'node_name': '20:00:00:de:fb:b1:86:a0'}]
            >>>

        """
        if self.__swobj.npv:
            cmd = "show npv flogi-table"
            out = self.__swobj.show(cmd, raw_text=True)
            return out
        cmd = "show flogi database"
        # if condition and params might not be needed, just added since there were options on switch
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        elif interface is not None:
            cmd += " interface " + str(interface)
        elif fcid is not None:
            cmd += " fcid " + str(fcid)
        out = self.__swobj.show(cmd)
        if out:
            if not self.__swobj.is_connection_type_ssh():
                return out["TABLE_flogi_entry"]["ROW_flogi_entry"]
            return out
        else:
            return {}

    @property
    def quiesce(self):
        """
        get quiesce or
        set quiesce

        :getter:
        :return: timeout value
        :rtype: int

        :example:
            >>> print(flogi_obj.quiesce)
            1
            >>>

        :setter:
        :param value: timeout value to be set ranging between 0 to 20000 milliseconds
        :type value: int

        :example:
            >>> flogi_obj.quiesce = 5
            >>>

        """
        cmd = "show flogi internal info"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "Stats: fs_flogi_quiesce_timerval:\s+(?P<val>\d+)"
        match = re.search(pat, "".join(out))
        if match:
            return int(match.groupdict()["val"])
        return None

    @quiesce.setter
    def quiesce(self, value):
        cmd = "flogi quiesce timeout " + str(value)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    @property
    def scale(self):
        """
        get scale or
        set scale

        :getter:
        :return: returns True if flogi scale enhancements is enabled, otherwise returns Flase
        :rtype: bool

        :example:
            >>> print(flogi_obj.scale)
            True
            >>>

        :setter:
        :param value: True/False to enable/disable flogi scale enhancements
        :type value: bool

        :example:
            >>> flogi_obj.scale = False
            >>>

        """
        cmd = "show flogi internal info"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "Stats: fs_flogi_scale_enabled:\s+(?P<val>\d+)"
        match = re.search(pat, "".join(out))
        if match:
            if match.groupdict()["val"] == "1":
                return True
            else:
                return False

    @scale.setter
    def scale(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "flogi scale enable"
        if not value:
            cmd = "no " + cmd
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    # TODO npv
