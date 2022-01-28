import logging
import re

from .connection_manager.errors import (
    InvalidAnalyticsType,
    InvalidInterface,
    UnsupportedSwitch,
    FeatureNotEnabled
)
from .constants import SHUTDOWN, NO_SHUTDOWN, PAT_FC, VALID_PIDS_MDS
from .interface import Interface
from .transceiver import Transceiver

log = logging.getLogger(__name__)


class Fc(Interface):
    """
    Fc interface module

    :param switch: switch object
    :type switch: Switch
    :param name: name of fc interface
    :type name: str
    :raises InvalidInterface: when interface name is incorrect
    :example:
        >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")

    """

    def __init__(self, switch, name):
        fcmatch = re.match(PAT_FC, name)
        if not fcmatch:
            raise InvalidInterface(
                "Interface name "
                + str(name)
                + " is not correct, name must be 'fc' interface. Example: 'fc1/2'.. fcobj = Fc(switch_obj,'fc1/2') "
            )
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

        super().__init__(switch, name)
        self.__swobj = switch
        self._swobj = switch

    # property for out_of_service
    def _set_out_of_service(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = (
                "terminal dont-ask ; interface "
                + self.name
                + " ; out-of-service force ; no terminal dont-ask "
        )
        if value:
            # First shutdown the port then
            self.status = SHUTDOWN
            self.__swobj.config(cmd)
        else:
            cmd = cmd.replace("out-of-service", "no out-of-service")
            self.__swobj.config(cmd)
            self.status = NO_SHUTDOWN

    # out_of_service property
    out_of_service = property(fset=_set_out_of_service)
    """
    set out-of-service configuration for the fc interface

    :param value: set to True to enable out-of-service, False otherwise
    :type value: bool
    :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> fcobj.out_of_service = True
            >>>
    """

    @property
    def transceiver(self):
        """
        Returns handler for transceiver module, using which we could do transceiver related operations

        :return: transceiver handler
        :rtype: Transceiver
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> trans_handler = fcobj.transceiver
            >>>
        """

        return Transceiver(self)

    @property
    def analytics_type(self):
        """
        get analytics type on the fc interface or
        set analytics type on the fc interface

        :getter:
        :return: analytics type on the interface, None if there are no analytics configs
        :rtype: str
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> print(fcobj.analytics_type)
            scsi
            >>>

        :setter:
        :param type: set analytics type on the fc interface
        :type type: str
        :values: scsi/nvme/all/None . Setting the value to None will remove the analytics config on the interface
        :example:
            >>> fcobj = Fc(switch = switch_obj, name = "fc1/1")
            >>> fcobj.analytics_type = 'scsi'
            scsi
            >>>

        """
        is_scsi = False
        is_nvme = False
        pat = "analytics type fc-(.*)"
        cmd = "show running-config interface " + self.name + " | grep analytics "
        out = self.__swobj.show(cmd, use_ssh=True)

        for eachline in out:
            newline = eachline.strip().strip("\n")
            m = re.match(pat, newline)
            if m:
                type = m.group(1)
                if type == "scsi":
                    is_scsi = True
                if type == "nvme":
                    is_nvme = True
        if is_scsi:
            if is_nvme:
                return "all"
            else:
                return "scsi"
        elif is_nvme:
            return "nvme"
        else:
            return None

    @analytics_type.setter
    def analytics_type(self, type):
        if not self.__swobj.feature("analytics"):
            raise FeatureNotEnabled("Analytics feature is not enabled")
        if type is None:
            cmd = "no analytics type fc-all"
        elif type == "scsi":
            cmd = "analytics type fc-scsi"
        elif type == "nvme":
            cmd = "analytics type fc-nvme"
        elif type == "all":
            cmd = "analytics type fc-all"
        else:
            raise InvalidAnalyticsType(
                "Invalid analytics type:('"
                + type
                + ")'. Valid types are scsi,nvme,all,None(to disable any analytics type)"
            )
        cmdtosend = "interface " + self.name + " ; " + cmd
        self.__swobj.config(cmdtosend)

    def _execute_transceiver_cmd(self):
        result = {}
        cmd = "show interface " + self.name + " transceiver detail"
        if self.__swobj.is_connection_type_ssh():
            return self.__swobj.show(cmd)
        retout = self.__swobj.show(cmd)["TABLE_interface_trans"]["ROW_interface_trans"]
        if type(retout) is list:
            rowout = retout[0]
        else:
            rowout = retout
        rowcalib = rowout["TABLE_calib"]["ROW_calib"]
        if type(rowcalib) is list:
            out = rowcalib[0]
        else:
            out = rowcalib
        if type(out) is list:
            for d in out:
                result.update(d)
        else:
            result = out
        return result
