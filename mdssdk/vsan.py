import logging
import re

from .connection_manager.errors import (
    CLIError,
    VsanNotPresent,
    InvalidInterface,
    UnsupportedSwitch,
)
from .constants import PAT_FC, PAT_PC, VALID_PIDS_MDS
from .fc import Fc
from .nxapikeys import vsankeys
from .parsers.vsan import ShowVsan, ShowVsanMembership
from .portchannel import PortChannel
from .utility.utils import get_key

log = logging.getLogger(__name__)


class Vsan(object):
    """

    Vsan module

    :param switch: switch object on which vsan operations need to be executed
    :type switch: Switch
    :param id: vsan id
    :type id: int

    :example:
        >>> vsan_obj = Vsan(switch=switch_obj, id=2)

    .. warning:: id must be within range 1-4094 (4079,4094 are reserved)

    """

    def __init__(self, switch, id):
        self.__swobj = switch
        self._id = id
        self._SW_VER = switch._SW_VER
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

    @property
    def id(self):
        """
        Get vsan id

        :return: id of the vsan if vsan is present on the switch, otherwise returns None
        :rtype: int
        :range: 1 to 4094

        """
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show("show vsan")
            shvsan = ShowVsan(outlines, self._id)
            return shvsan.id
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        vid = out[get_key(vsankeys.VSAN_ID, self._SW_VER)]
        if type(vid) is str:
            return int(vid)
        else:
            return vid

    @property
    def name(self):
        """
        Get the name of the vsan or
        Set the name of the vsan

        :getter:
        :return: name of the vsan,
                 returns None if vsan is not present on the switch
        :rtype: str
        :example:
            >>> print(vsan_obj.name)
            "VSAN0001"
            >>>

        :setter:
        :param name: name of the vsan
        :type name: str

        :example:
            >>> vsan_obj.name = "vsan_2"

        """
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show("show vsan")
            shvsan = ShowVsan(outlines, self._id)
            return shvsan.name
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        if out:
            return out.get(get_key(vsankeys.VSAN_NAME, self._SW_VER))
        return None

    @name.setter
    def name(self, name):
        self.create(name)

    @property
    def state(self):
        """
        Get the state of the vsan

        :return: state of the vsan
                 returns None if vsan is not present on the switch
        :values: return values are either 'active' or 'suspended'

        """
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show("show vsan")
            shvsan = ShowVsan(outlines, self._id)
            return shvsan.state
        try:
            out = self.__get_facts()
        except VsanNotPresent:
            return None
        if out:
            return out.get(get_key(vsankeys.VSAN_STATE, self._SW_VER))
        return None

    @property
    def interfaces(self):
        if self.id is None:
            return None
        cmd = "show vsan " + str(self._id) + " membership"
        allint = []
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show(cmd)
            shvsan = ShowVsanMembership(outlines)
            allint = shvsan.interfaces
        else:
            out = self.__swobj.show(cmd)["TABLE_vsan_membership"]["ROW_vsan_membership"]
            if type(out) is list:
                out = out[0]
            allint = out.get("interfaces", None)
        if allint is None:
            return None
        else:
            retelements = []
            if type(allint) is str:
                allintnames = [allint]
            else:
                allintnames = allint
            for eachintname in allintnames:
                fcmatch = re.match(PAT_FC, eachintname)
                pcmatch = re.match(PAT_PC, eachintname)
                if fcmatch:
                    intobj = Fc(switch=self.__swobj, name=eachintname)
                elif pcmatch:
                    id = pcmatch.group(1)
                    intobj = PortChannel(switch=self.__swobj, id=int(id))
                else:
                    log.error(
                        "Unsupported interface "
                        + eachintname
                        + " , hence skipping it, this type of interface is not supported yet"
                    )
                retelements.append(intobj)
            return retelements

    # property for suspend
    def _set_suspend(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "vsan database ; "
        if value:
            cmd = cmd + "vsan " + str(self._id) + " suspend"
        else:
            cmd = cmd + "no vsan " + str(self._id) + " suspend"

        self.__swobj.config(cmd)

    # suspend property
    suspend = property(fset=_set_suspend)
    """
    Set the state of the vsan

    :setter:
    :param value: if true suspends the vsan, else does a 'no suspend' 
    :type value: bool
    :raises TypeError: If the passed value is not of type bool

    :example:
        >>> vsan_obj.suspend = True

    """

    def create(self, name=None):
        """
        Creates vsan on the switch

        :param name: name of vsan (optional parameter, defaults to 'VSAN<vsan-id>' if passed as None)
        :type name: str or None
        :return: None

        :example:
            >>> vsan_obj.create("vsan_2")

        """

        cmd = "vsan database ; vsan " + str(self._id)
        if name is not None:
            cmd = cmd + " name '" + name + "'"
        self.__swobj.config(cmd)

    def delete(self):
        """Deletes the vsan on the switch

        :param: None
        :return: None
        :raises VsanNotPresent: if vsan is not present on the switch

        :example:
            >>> vsan_obj.delete()

        """

        try:
            cmd = "terminal dont-ask ; " "vsan database ; " "no vsan " + str(self._id)
            self.__swobj.config(cmd)
        except CLIError as c:
            cmddontask = "no terminal dont-ask"
            self.__swobj.config(cmddontask)
            log.error(c)
            raise CLIError(cmd, c.message)
        finally:
            cmd = "no terminal dont-ask"
            self.__swobj.config(cmd)

    def add_interfaces(self, interfaces):
        """Add interfaces to the vsan

        :param interfaces: interfaces to be added to the vsan
        :type interfaces: list(Fc or PortChannel)
        :raises VsanNotPresent: if vsan is not present on the switch
        :raises InvalidInterface: if the interface is not among supported interface types (‘fc’ and ‘port-channel’)
        :raises CLIError: if the switch raises a error for the cli command passed
        :return: None

        :example:
            >>> fc = Fc(switch,"fc1/1")
            >>> pc = PortChannel(switch,1)
            >>> vsan_obj.add_interfaces([fc,pc])
            >>> vsan_obj.add_interfaces(fc)
            Traceback (most recent call last):
            ...
            TypeError: Fc object is not iterable

        """

        if self.id is None:
            raise VsanNotPresent(
                "Vsan " + str(self._id) + " is not present on the switch."
            )
        else:
            cmd = ""
            for eachint in interfaces:
                fcmatch = re.match(PAT_FC, eachint.name)
                pcmatch = re.match(PAT_PC, eachint.name)
                if fcmatch or pcmatch:
                    cmd = (
                            cmd
                            + "terminal dont-ask ; vsan database ; vsan "
                            + str(self._id)
                            + " interface "
                            + eachint.name
                            + " ; no terminal dont-ask ; "
                    )
                    # cmdlist.append(cmd)
                else:
                    raise InvalidInterface(
                        "Interface "
                        + str(eachint.name)
                        + " is not supported, and hence cannot be added to the vsan, "
                          "supported interface types are 'fc' amd 'port-channel'"
                    )
            try:
                # self.__swobj._config_list(cmdlist)
                self.__swobj.config(cmd)
            except CLIError as c:
                if (
                        "membership being configured is already configured for the interface"
                        in c.message
                ):
                    return
                else:
                    log.error(c)
                    raise CLIError(cmd, c.message)

    def __get_facts(self):
        shvsan = self.__swobj.show("show vsan")

        listofvsaninfo = shvsan["TABLE_vsan"]["ROW_vsan"]
        vsanlist = []
        for eachv in listofvsaninfo:
            vsanlist.append(str(eachv[get_key(vsankeys.VSAN_ID, self._SW_VER)]))
        if str(self._id) not in vsanlist:
            raise VsanNotPresent(
                "Vsan " + str(self._id) + " is not present on the switch."
            )

        shvsan_req_out = {}

        # Parse show vsan json output
        for eachele in listofvsaninfo:
            if str(eachele[get_key(vsankeys.VSAN_ID, self._SW_VER)]) == str(self._id):
                shvsan_req_out = eachele
                break
        if not shvsan_req_out:
            return None

        return dict(shvsan_req_out)
