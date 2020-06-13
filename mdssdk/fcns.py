import logging

from .connection_manager.errors import CLIError

log = logging.getLogger(__name__)

class Fcns(object):
    
    def __init__(self, switch):
        self.__swobj = switch

    def database(self, vsan = None, fcid = None, detail = False):
        cmd = "show fcns database"
        if fcid is not None:
            cmd += " fcid "+str(fcid)
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan "+str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            return out['TABLE_fcns_vsan']['ROW_fcns_vsan']
        else:
            return None

    def statistics(self, vsan = None, detail = False):
        cmd = "show fcns statistics"
        if detail:
            cmd += " detail"
        if vsan is not None:
            cmd += " vsan "+str(vsan)
        out = self.__swobj.show(cmd)
        if out:
            return out['TABLE_fcns_vsan']['ROW_fcns_vsan']
        else:
            return None

    def _set_bulk_notify(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        if value:
            cmd = "no fcns no-bulk-notify"
        else:
            cmd = "terminal dont-ask ; fcns no-bulk-notify"
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])
        self.__swobj.config("no terminal dont-ask")

    bulk_notify = property(fset=_set_bulk_notify)
    # for getter, didn't find command

    def _set_zone_lookup_cache(self,value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "fcns zone-lookup-cache"
        if not value:
            cmd = "no "+cmd
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])

    zone_lookup_cache = property(fset=_set_zone_lookup_cache)
    # for getter, didn't find command
    
    def proxy_port(self, pwwn, vsan):
        cmd = "fcns proxy-port "+str(pwwn)+" vsan "+str(vsan)
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])
            
    def no_auto_poll(self, vsan = None, pwwn = None):
        cmd = "fcns no-auto-poll"
        if vsan is not None:
            cmd += " vsan "+str(vsan)
        elif pwwn is not None:
            cmd += " wwn "+str(pwwn)
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])
         
    def reject_duplicate_pwwn(self, vsan):
        cmd = "fcns reject-duplicate-pwwn vsan "+str(vsan)
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])

    # TODO 
