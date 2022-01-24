import logging
import re

from .connection_manager.errors import CLIError
from .connection_manager.errors import InvalidProfile

log = logging.getLogger(__name__)


class Fdmi:
    """
    Fdmi Module

    :example:
        >>> switch_obj = Switch(ip_address = switch_ip, username = switch_username, password = switch_password )
        >>> fdmi_hand = switch_obj.fdmi()
        >>> print(fdmi_hand)
        <mdslib.analytics.Analytics object at 0x10ad710d0>

    """

    def __init__(self, switch, hbaid=None, vsan=None):
        ERR1 = "ERROR!!! vsan argument cant be empty while passing hbaid argument. Please pass both hbaid and vsan or only vsan"
        self._sw = switch
        self._hbaid = hbaid
        self._vsan = vsan
        self._alldata = []
        if self._hbaid is None:
            if self._vsan is None:
                cmd = "show fdmi database detail"
            else:
                cmd = "show fdmi database detail vsan " + str(self._vsan)
        else:
            if self._vsan is None:
                print(ERR1)
                exit()
            else:
                cmd = "show fdmi database detail hba-id " + self._hbaid + " vsan " + str(self._vsan)
        out = self._sw.show(cmd)
        if self._sw.is_connection_type_ssh():
            self._alldata = out
        else:
            if out:
                reqout = out["TABLE_vsan"]["ROW_vsan"]
                if type(reqout) is dict:
                    all_reqout = [reqout]
                else:
                    all_reqout = reqout
                for reqout in all_reqout:
                    vk = "vsan"
                    vsan = reqout[vk]
                    hbadata = reqout["TABLE_hba_id"]["ROW_hba_id"]
                    for each_hbadata in hbadata:
                        piddata = each_hbadata.get("TABLE_port_id", {})
                        # print(piddata)
                        if piddata:
                            reqpiddata = piddata["ROW_port_id"][0]
                            each_hbadata.pop("TABLE_port_id")
                            tmp = {}
                            tmp[vk] = vsan
                            # print(tmp)
                            # print(each_hbadata)
                            # print(reqpiddata)
                            # print(reqout)
                            newdict = {**tmp, **each_hbadata, **reqpiddata}
                            self._alldata.append(newdict)
        print(self._alldata)

    def hba_list(self, vsan=None):
        pass
