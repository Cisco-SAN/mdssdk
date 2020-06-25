import logging
import re

from .connection_manager.errors import CLIError

log = logging.getLogger(__name__)


class Fcns(object):
    def __init__(self, switch):
        self.__swobj = switch

    def database(self, vsan=None, fcid=None, detail=False):
        """
        Get fcns database
        
        :param vsan: id of vsan (optional parameter, defaults to None)
        :type vsan: int or None
        :param fcid: fcid (optional parameter, defaults to None)
        :type fcid: str or None
        :param detail: detail (optional parameter, defaults to False)
        :type detail: bool
        :return: fcns database
        :rtype: list
        :example:
            >>> fcns_obj = Fcns(switch_obj)
            >>> print(fcns_obj.database())
            >>>

        """
        cmd = "show fcns database"
        if fcid is not None:
            cmd += " fcid " + str(fcid)
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            if not self.__swobj.is_connection_type_ssh():
                return out["TABLE_fcns_vsan"]["ROW_fcns_vsan"]
            else:
                if type(out[0]) is str:
                    if ("vsan not present"== out[0].strip()):
                        return {}
            return out
        else:
            return {}

    def statistics(self, vsan=None, detail=False):
        """
        Get fcns statistics
        
        :param vsan: id of vsan (optional parameter, defaults to None)
        :type vsan: int or None
        :param detail: detail (optional parameter, defaults to False)
        :type detail: bool
        :return: fcns statistics
        :rtype: list
        :example:
            >>> fcns_obj = Fcns(switch_obj)
            >>> print(fcns_obj.statistics())
            >>>

        """
        cmd = "show fcns statistics"
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            if not self.__swobj.is_connection_type_ssh():
                return out["TABLE_fcns_vsan"]["ROW_fcns_vsan"]
            else:
                if type(out[0]) is str:
                    if ("vsan not present"== out[0].strip()):
                        return {}
            return out
        else:
            return {}

    @property
    def no_bulk_notify(self):
        """
        get no_bulk_notify or
        set no_bulk_notify

        :getter:
        :return: returns True if bulk notification for db changes is disabled, otherwise returns False 
        :rtype: bool

        :example:
            >>> print(fcns_obj.no_bulk_notify)
            True
            >>>

        :setter:
        :param value: True/False to disable/enable bulk notification for db changes
        :type value: bool

        :example:
            >>> fcns_obj.no_bulk_notify = False
            >>>

        """
        cmd = "show running section fcns"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "fcns no-bulk-notify"
        match = re.search(pat, "".join(out))
        if match:
            return True
        else:
            return False

    @no_bulk_notify.setter
    def no_bulk_notify(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        if value:
            cmd = "terminal dont-ask ; fcns no-bulk-notify"
        else:
            cmd = "no fcns no-bulk-notify"
        try:
            out = self.__swobj.config(cmd)
        except CLIError as c:
            if "FCNS bulk notification optimization is necessary" in c.message:
                log.debug(c.message)
            else:
                raise CLIError(cmd, c.message)
        self.__swobj.config("no terminal dont-ask")

    @property
    def zone_lookup_cache(self):
        """
        get zone_lookup_cache or
        set zone_lookup_cache

        :getter:
        :return: returns True if db uses Zone Lookup cache for NS queries, otherwise returns False 
        :rtype: bool

        :example:
            >>> print(fcns_obj.zone_lookup_cache)
            True
            >>>

        :setter:
        :param value: True/False to enable/disable use of Zone Lookup cache for NS queries
        :type value: bool

        :example:
            >>> fcns_obj.zone_lookup_cache = False
            >>>

        """
        cmd = "show running section fcns"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "fcns zone-lookup-cache"
        match = re.search(pat, "".join(out))
        if match:
            return True
        else:
            return False

    @zone_lookup_cache.setter
    def zone_lookup_cache(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "fcns zone-lookup-cache"
        if not value:
            cmd = "no " + cmd
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    def proxy_port(self, pwwn, vsan):
        """
        Configure proxy port
        
        :param pwwn: pwwn 
        :type pwwn: str
        :param name: id of vsan 
        :type name: int 
        :return: None
        :example:
            >>> fcns_obj = Fcns(switch_obj)
            >>> print(fcns_obj.proxy_port(vsan = 1, pwwn = "10:00:00:de:fb:b1:86:a1"))
            >>>

        """
        cmd = "fcns proxy-port " + str(pwwn) + " vsan " + str(vsan)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    def no_auto_poll(self, vsan=None, pwwn=None):
        """
        Disable auto polling
        
        :param name: id of vsan (optional parameter, defaults to None)
        :type name: int or None
        :param pwwn: pwwn (optional parameter, defaults to None)
        :type pwwn: str or None
        :return: None
        :example:
            >>> fcns_obj = Fcns(switch_obj)
            >>> print(fcns_obj.no_auto_poll())
            >>>

        """
        cmd = "fcns no-auto-poll"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        elif pwwn is not None:
            cmd += " wwn " + str(pwwn)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    def reject_duplicate_pwwn(self, vsan):
        """
        Reject logging of ports with duplicate pwwn
        
        :param vsan: id of vsan 
        :type vsan: int
        :return: None
        :example:
            >>> fcns_obj = Fcns(switch_obj)
            >>> print(fcns_obj.reject_duplicate_pwwn(vsan = 1))
            >>>

        """
        cmd = "fcns reject-duplicate-pwwn vsan " + str(vsan)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    # TODO: ssh and https outputs for database and statistics vary slightly in nested TABLE tags