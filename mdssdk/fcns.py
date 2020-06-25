import logging
import re

from .connection_manager.errors import CLIError

log = logging.getLogger(__name__)


class Fcns(object):
    def __init__(self, switch):
        self.__swobj = switch

    def database(self, vsan=None, fcid=None, detail=False):
        cmd = "show fcns database"
        if fcid is not None:
            cmd += " fcid " + str(fcid)
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            return out["TABLE_fcns_vsan"]["ROW_fcns_vsan"]
        else:
            return None

    def statistics(self, vsan=None, detail=False):
        cmd = "show fcns statistics"
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            return out["TABLE_fcns_vsan"]["ROW_fcns_vsan"]
        else:
            return None

    @property
    def no_bulk_notify(self):
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
        cmd = "fcns proxy-port " + str(pwwn) + " vsan " + str(vsan)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    def no_auto_poll(self, vsan=None, pwwn=None):
        cmd = "fcns no-auto-poll"
        if vsan is not None:
            cmd += " vsan " + str(vsan)
        elif pwwn is not None:
            cmd += " wwn " + str(pwwn)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    def reject_duplicate_pwwn(self, vsan):
        cmd = "fcns reject-duplicate-pwwn vsan " + str(vsan)
        out = self.__swobj.config(cmd)
        if out:
            raise CLIError(cmd, out[0]["msg"])

    # TODO
