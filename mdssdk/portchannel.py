import logging
import re

from .connection_manager.errors import (
    PortChannelNotPresent,
    InvalidPortChannelRange,
    InvalidChannelMode,
    CLIError,
    UnsupportedSwitch,
)
from .constants import ON, ACTIVE, PAT_FC, PAT_PC, VALID_PC_RANGE, VALID_PIDS_MDS
from .fc import Fc
from .interface import Interface
from .nxapikeys import portchanelkeys
from .parsers.portchannel import ShowPortChannelDatabase, ShowPortChannelDatabaseDetail
from .utility.utils import get_key

log = logging.getLogger(__name__)


class PortChannel(Interface):
    """
    PortChannel interface module
    extends Interface module

    :param switch: switch object
    :type switch: Switch
    :param id: id of port-channel interface
    :type id: int
    :raises InvalidPortChannelRange: when it is not within 1 to 256
    :example:
        >>> pcobj = PortChannel(switch = switch_obj, id = 1)

    """

    def __init__(self, switch, id):
        if id not in VALID_PC_RANGE:
            raise InvalidPortChannelRange(
                "Port channel id "
                + str(id)
                + " is invalid, id should range from "
                + str(VALID_PC_RANGE[0])
                + " to "
                + str(VALID_PC_RANGE[-1])
            )
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

        self._id = id
        name = "port-channel" + str(self._id)

        # First set the port-channel id and name and then call the base class init
        super().__init__(switch, name)
        self.__swobj = switch

    @property
    def id(self):
        """
        Returns port-channel id

        :return: id of port-channel
        :rtype: int
        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> print(pcobj.id)
            1
            >>>
        """

        return self._id

    @property
    def channel_mode(self):
        """
        set or get the channel mode of the port-channel

        :getter:
        :return: Returns the channel mode of the port-channel
        :rtype: str
        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> print(pcobj.channel_mode)
            active
            >>>

        :setter:
        :param mode: mode to which port-channel mode needs to be set
        :type mode: str
        :values: 'on', 'active'
        :raises InvalidChanelMode: if mode is not 'on' or 'active'
        :raises PortChannelNotPresent: if port-channel is not present on the switch
        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> pcobj.channel_mode = 'active'
            >>>

        """

        if not self.__is_pc_present():
            return None
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show(
                "show port-channel database detail interface port-channel "
                + str(self._id)
            )
            shpc = ShowPortChannelDatabaseDetail(outlines)
            return shpc.channel_mode
        detailout = self.__get_pc_facts()
        self.__admin_ch_mode = detailout[
            get_key(portchanelkeys.ADMIN_CHN_MODE, self._SW_VER)
        ]
        memdetail = detailout.get("TABLE_port_channel_member_detail", None)
        if memdetail is None:
            return self.__admin_ch_mode
        else:
            allmem = memdetail["ROW_port_channel_member_detail"]
            if type(allmem) is dict:
                # it means there is only one port member in the port-channel
                return allmem[get_key(portchanelkeys.OPER_CHN_MODE, self._SW_VER)]
            else:
                # it means there is more than one member in the port-channel
                # get one of the member in the port-channel and return its channel mode
                onemem = allmem[0]
                return onemem[get_key(portchanelkeys.OPER_CHN_MODE, self._SW_VER)]

    @channel_mode.setter
    def channel_mode(self, mode):
        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel "
                + str(self._id)
                + " is not present on the switch, please create the PC first"
            )
        mode = mode.lower()
        cmd = "interface port-channel " + str(self._id)
        if mode == ACTIVE:
            cmd = cmd + " ; channel mode active"
        elif mode == ON:
            cmd = cmd + " ; no channel mode active"
        else:
            raise InvalidChannelMode(
                "Invalid channel mode ("
                + str(mode)
                + "), Valid values are: "
                + ON
                + ","
                + ACTIVE
            )
        self.__swobj.config(cmd)

    @property
    def members(self):
        """
        Get the members of the port-channel

        :return: members of the port-channel in dictionary format
        :rtype: dict(name: obj(Fc))
        """

        if not self.__is_pc_present():
            return {}
        if self.__swobj.is_connection_type_ssh():
            outlines = self.__swobj.show(
                "show port-channel database detail interface port-channel "
                + str(self._id)
            )
            shpc = ShowPortChannelDatabaseDetail(outlines)
            memdetail = shpc.members
            if memdetail is None:
                return {}
            else:
                allintnames = []
                for eachmem in memdetail:
                    allintnames.append(eachmem["port"])
        else:
            detailout = self.__get_pc_facts()
            memdetail = detailout.get("TABLE_port_channel_member_detail", None)
            if memdetail is None:
                return {}
            else:
                allintnames = []
                allmem = memdetail["ROW_port_channel_member_detail"]
                if type(allmem) is dict:
                    # it means there is only one port member in the port-channel
                    allintnames.append(
                        allmem[get_key(portchanelkeys.PORT, self._SW_VER)]
                    )
                else:
                    # it means there is more than one member in the port-channel
                    # get the one of the member in the port-channel and return its channel mode
                    for eachmem in allmem:
                        allintnames.append(
                            eachmem[get_key(portchanelkeys.PORT, self._SW_VER)]
                        )
        retelements = {}
        for eachintname in allintnames:
            fcmatch = re.match(PAT_FC, eachintname)
            if fcmatch:
                intobj = Fc(switch=self.__swobj, name=eachintname)
                retelements[eachintname] = intobj
            else:
                log.error(
                    "Unsupported interface "
                    + eachintname
                    + " , hence skipping it, this type of interface is not supported yet"
                )
        return retelements

    def create(self):
        """
        Creates port-channel on switch

        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> pcobj.create()
        """

        cmd = "interface port-channel " + str(self._id)
        self.__swobj.config(cmd)

    def delete(self):
        """
        Deletes port-channel on switch

        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> pcobj.delete()
        """

        if self.__is_pc_present():
            cmd = "no interface port-channel " + str(self._id)
            try:
                self.__swobj.config(cmd)
            except CLIError as c:
                if (
                        not "port-channel "
                            + str(self._id)
                            + " deleted and all its members disabled"
                            in c.message
                ):
                    raise CLIError(cmd, c.message)

    def add_members(self, interfaces):
        """
        Add Fc members to the port channel

        :param interfaces: list of Fc interfaces to be added
        :type interfaces: list(Fc)
        :raises PortChannelNotPresent: if port channel is not present on switch

        :example:
            >>> pcobj = PortChannel(switch = switch_obj, id = 1)
            >>> pcobj.create()
            >>> fc1 = Fc( switch = switch_obj, name = "fc1/1")
            >>> fc2 = Fc( switch = switch_obj, name = "fc1/2")
            >>> pcobj.add_members([fc1,fc2])
            >>>

        """

        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel "
                + str(self._id)
                + " is not present on the switch, please create the PC first"
            )
        for eachint in interfaces:
            cmd = (
                    "interface "
                    + eachint.name
                    + " ; channel-group "
                    + str(self._id)
                    + " force "
            )
            try:
                out = self.__swobj.config(cmd)
            except CLIError as c:
                if (
                        str(eachint.name)
                        + " added to port-channel "
                        + str(self._id)
                        + " and disabled"
                        in c.message
                ):
                    continue
                raise CLIError(cmd, c.message)

    def remove_members(self, interfaces):
        """
        Remove Fc members from the port channel

        :param interfaces: list of Fc interfaces to be removed
        :type interfaces: list(Fc)
        :raises PortChannelNotPresent: if port channel is not present on switch

        :example:
            >>>
            >>> pcobj.remove_members([fc1,fc2])
            >>>

        """
        if not self.__is_pc_present():
            raise PortChannelNotPresent(
                "Port channel "
                + str(self._id)
                + " is not present on the switch, please create the PC first"
            )

        for eachint in interfaces:
            cmd = "interface " + eachint.name + " ; no channel-group " + str(self._id)
            try:
                out = self.__swobj.config(cmd)
            except CLIError as c:
                if "please do the same operation on the switch" in c.message:
                    continue
                raise CLIError(cmd, c.message)

    def __get_pc_facts(self):
        cmd = "show port-channel database detail interface port-channel " + str(
            self._id
        )
        out = self.__swobj.show(cmd)
        detailoutput = out["TABLE_port_channel_database"]["ROW_port_channel_database"]
        if type(detailoutput) is list:
            detailoutput = detailoutput[0]
        return detailoutput

    def __is_pc_present(self):
        cmd = "show port-channel database"
        out = self.__swobj.show(cmd)
        if self.__swobj.is_connection_type_ssh():
            shpc = ShowPortChannelDatabase(out, self._id)
            return shpc.present
        if out:
            # There is atleast one PC in the switch
            pcdb = out["TABLE_port_channel_database"]["ROW_port_channel_database"]
            if type(pcdb) is dict:
                # There is only one PC in the switch
                pcdblist = [pcdb]
            else:
                # There are multiple PC in the switch
                pcdblist = pcdb
            for eachpc in pcdblist:
                pcname = eachpc[get_key(portchanelkeys.INT, self._SW_VER)]
                pcmatch = re.match(PAT_PC, pcname)
                if pcmatch:
                    pcid = pcmatch.group(1).strip()
                    if int(pcid) == self._id:
                        return True
            return False
        else:
            # There are no PC in the switch
            return False
