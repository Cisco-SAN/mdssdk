import logging

import time

from .connection_manager.errors import CLIError, InvalidMode, UnsupportedSwitch
from .constants import ENHANCED, BASIC, VALID_PIDS_MDS
from .nxapikeys import devicealiaskeys
from .parsers.device_alias import ShowDeviceAliasDatabase, ShowDeviceAliasStatus
from .utility.utils import get_key

log = logging.getLogger(__name__)


class DeviceAlias(object):
    """
    Device Alias module

    :param switch: switch object on which device-alias operations needs to be executed
    :type switch: Switch

    :example:
        >>> da = DeviceAlias(switch = switch_obj)

    """

    def __init__(self, switch):
        self.__swobj = switch
        self._SW_VER = switch._SW_VER
        if not switch.product_id.startswith(VALID_PIDS_MDS):
            raise UnsupportedSwitch(
                "Unsupported Switch. Current support of this class is only for MDS only switches."
            )

    @property
    def mode(self):
        """
        set device-alias mode or
        get device-alias mode

        :getter:
        :return: mode
        :rtype: str
        :values: ['basic', 'enhanced']
        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> print(da.mode)
            enhanced
            >>>

        :setter:
        :param mode: mode
        :type mode: str
        :values: ['basic', 'enhanced']
        :raises InvalidMode: if mode is not to either 'basic' or 'enhanced'
        :raises CLIError: If there is any cli error
        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.mode = 'basic'
            >>>

        """
        if self.__swobj.is_connection_type_ssh():
            cmd = "show device-alias status"
            outlines = self.__swobj.show(cmd)
            shdasta = ShowDeviceAliasStatus(outlines)
            return shdasta.mode.lower()
        facts_out = self.__get_facts()
        return self.__get_mode(facts_out)

    @mode.setter
    def mode(self, mode):
        log.debug("Setting device alias mode to " + mode)
        if mode.lower() == ENHANCED:
            cmd = "device-alias database ; device-alias mode enhanced"
        elif mode.lower() == BASIC:
            cmd = "device-alias database ; no device-alias mode enhanced"
        else:
            raise InvalidMode(
                "Invalid device alias mode: "
                + str(mode)
                + ". Valid values are "
                + ENHANCED
                + ","
                + BASIC
            )
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            self.__clear_lock_if_distribute()
            raise CLIError(*c.args)
        # There is no error
        self.__send_commit()

    @property
    def distribute(self):
        """
        set device-alias distribute configuration or
        get device-alias distribute configuration

        :getter:
        :return: distribute
        :rtype: bool
        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> print(da.distribute)
            True
            >>>

        :setter:
        :param distribute: set to True if distribute needs to be enabled or set to False if distribute needs to be disabled
        :type distribute: bool
        :raises CLIError: If there is any cli command error
        :raises TypeError: If the passed value is not of type bool

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.distribute = True
            >>>

        """

        if self.__swobj.is_connection_type_ssh():
            cmd = "show device-alias status"
            outlines = self.__swobj.show(cmd)
            shdasta = ShowDeviceAliasStatus(outlines)
            dis = shdasta.distribute
        else:
            facts_out = self.__get_facts()
            dis = self.__get_distribute(facts_out)

        if dis.lower() == "enabled":
            return True
        else:
            return False

    @distribute.setter
    def distribute(self, distribute):
        if type(distribute) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        if distribute:
            cmd = "device-alias database ; device-alias distribute"
            log.debug("Setting device alias mode to 'Enabled'")
        else:
            cmd = "device-alias database ; no device-alias distribute"
            log.debug("Setting device alias mode to 'Disabled'")
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            self.__clear_lock_if_distribute()
            raise CLIError(*c.args)
        # There is no error
        self.__send_commit()

    @property
    def locked(self):
        """
        Check if device-alias has acquired lock or not

        :return: locked: Returns True if device-alias lock is acquired else returns False
        :rtype: bool
        """

        if self.__swobj.is_connection_type_ssh():
            cmd = "show device-alias status"
            outlines = self.__swobj.show(cmd)
            shdasta = ShowDeviceAliasStatus(outlines)
            lock_user = shdasta.locked_user
        else:
            facts_out = self.__get_facts()
            lock_user = self.__locked_user(facts_out)
        if lock_user is None:
            return False
        return True

    @property
    def database(self):
        """
        Returns device-alias database in dict(name:pwwn) format, if there are no device-alias entries then it returns None

        :return: database or None
        :rtype: dict(name:pwwn)
        """
        if self.__swobj.is_connection_type_ssh():
            cmd = "show device-alias database"
            outlines = self.__swobj.show(cmd)
            shdada = ShowDeviceAliasDatabase(outlines)
            return shdada.database

        retout = {}
        facts_out = self.__get_facts()
        allentries = facts_out.get("device_alias_entries", None)
        if allentries is None:
            # Means there are no entries
            return None
        else:
            if type(allentries) is dict:
                # That means there is only one entry in the database
                # hence we need to convert allentries to a list, if there are more than
                # one entry in the database then allentries will not be a dict it will be a list
                allentries = [allentries]
            for eachentry in allentries:
                retout[eachentry["dev_alias_name"]] = eachentry["pwwn"]
            return retout

    def create(self, namepwwn):
        """
        Create device alias entries

        :param namepwwn: name and pwwwn
        :type namepwwn: dict (name: pwwn)
        :return: None
        :raises CLIError: If there is any cli command error

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.create({'device1': '21:00:00:0e:1e:30:34:a5','device2': '21:00:00:0e:1e:30:3c:c5'})
            >>>
        """

        for name, pwwn in namepwwn.items():
            log.debug("Creating device alias with name:pwwn  " + name + " : " + pwwn)
            cmd = "device-alias database ; "
            cmd = cmd + " device-alias name " + name + " pwwn " + pwwn + " ; "
            try:
                out = self.__swobj.config(cmd)
            except CLIError as c:
                self.__clear_lock_if_distribute()
                raise CLIError(*c.args)
            # There is no error
            self.__send_commit()

    def delete(self, name):
        """
        Delete device alias entry

        :param name: name of device alias that needs to be deleted
        :type name: str
        :return: None
        :raises CLIError: If there is any cli command error

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.delete('device1')

        """

        log.debug("Deleting device alias with args " + name)
        cmd = "device-alias database ; no device-alias name " + name
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            self.__clear_lock_if_distribute()
            raise CLIError(*c.args)
        # There is no error
        self.__send_commit()

    def rename(self, oldname, newname):
        """
        Rename device alias entry

        :param oldname: old device alias name
        :type oldname: str
        :param newname: new device alias name
        :type newname: str
        :return: None
        :raises CLIError: If there is any cli command error

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.rename('device1','device_new')
            >>>

        """

        log.debug("Renaming device alias with args " + oldname + " " + newname)
        cmd = "device-alias database ; device-alias rename " + oldname + " " + newname
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            self.__clear_lock_if_distribute()
            raise CLIError(*c.args)
        # There is no error
        self.__send_commit()

    def clear_lock(self):
        """
        Clears lock if lock is acquired

        :param: None
        :return: None

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.clear_lock()
            >>>

        """

        cmd = "terminal dont-ask ; device-alias database ; clear device-alias session ; no terminal dont-ask "
        self.__swobj.config(cmd)

    def clear_database(self):
        """
        Clears database entries

        :param: None
        :return: None
        :raises CLIError: If there is any cli command error

        :example:
            >>>
            >>> da = DeviceAlias(switch = switch_obj)
            >>> da.clear_database()
            >>>

        """

        cmd = "terminal dont-ask ; device-alias database ; clear device-alias database ; no terminal dont-ask "
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            self.__clear_lock_if_distribute()
            raise CLIError(*c.args)
        # There is no error
        self.__send_commit()

    def __get_facts(self):
        log.debug("Getting device alias facts")
        retoutput = {}
        out = self.__swobj.show("show device-alias database")
        if out:
            num = out["number_of_entries"]
            da = out["TABLE_device_alias_database"]["ROW_device_alias_database"]

            retoutput["number_of_entries"] = num
            retoutput["device_alias_entries"] = da
        shdastatus = self.__swobj.show("show device-alias status")

        return dict(retoutput, **shdastatus)

    def __get_mode(self, facts_out):
        return facts_out[get_key(devicealiaskeys.MODE, self._SW_VER)]

    def __get_distribute(self, facts_out):
        return facts_out[get_key(devicealiaskeys.FABRIC_DISTRIBUTE, self._SW_VER)]

    def __locked_user(self, facts_out):
        locker_user = get_key(devicealiaskeys.LOCKED_USER, self._SW_VER)
        if locker_user in facts_out.keys():
            return facts_out[locker_user]
        else:
            return None

    def __send_commit(self):
        if self.distribute:
            cmd = "terminal dont-ask ; device-alias commit ; no terminal dont-ask "
            msg = None
            try:
                out = self.__swobj.config(cmd)
            except CLIError as c:
                msg = c.message
            if msg is not None:
                if (
                        "The following device-alias changes are about to be committed"
                        in msg
                ):
                    pass
                elif "There are no pending changes" in msg:
                    self.clear_lock()
                    log.debug(
                        "The commit command was not executed because Device Alias already present"
                    )
                elif "Commit in progress. Check the status." in msg:
                    log.info(
                        "Commit in progress...sleeping for 5 sec, please check again."
                    )
                    time.sleep(5)
                    self.__send_commit()
                elif "Device-alias enhanced zone member present" in msg:
                    self.clear_lock()
                    raise CLIError(cmd, msg)
                else:
                    self.clear_lock()
                    raise CLIError(cmd, msg)

    def __clear_lock_if_distribute(self):
        if self.distribute:
            self.clear_lock()
