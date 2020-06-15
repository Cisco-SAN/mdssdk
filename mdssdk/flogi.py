import logging
import re

from .connection_manager.errors import CLIError

log = logging.getLogger(__name__)

class Flogi(object):
    
    def __init__(self, switch):
        self.__swobj = switch

    def database(self, vsan = None, interface = None, fcid = None):
        if self.__swobj.npv:
            cmd = "show npv flogi-table"
            out = self.__swobj.show(cmd, raw_text=True)
            return out
        cmd = "show flogi database"
        # if condition and params might not be needed, just added since there were options on switch
        if vsan is not None:
            cmd += " vsan "+str(vsan) 
        elif interface is not None:
            cmd += " interface "+str(interface) 
        elif fcid is not None:
            cmd += " fcid "+str(fcid) 
        out = self.__swobj.show(cmd)
        if out :
            return out['TABLE_flogi_entry']['ROW_flogi_entry']
        else:
            return None
      
    @property
    def quiesce(self):
        cmd = "show flogi internal info"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "Stats: fs_flogi_quiesce_timerval:\s+(?P<val>\d+)"
        match = re.search(pat, "".join(out))
        if match:
            return int(match.groupdict()['val'])
        return None
  
    @quiesce.setter
    def quiesce(self, value):
        cmd = "flogi quiesce timeout "+str(value) 
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])
   
    @property
    def scale(self):
        cmd = "show flogi internal info"
        out = self.__swobj.show(cmd, raw_text=True)
        pat = "Stats: fs_flogi_scale_enabled:\s+(?P<val>\d+)"
        match = re.search(pat, "".join(out))
        if match:
            if match.groupdict()['val'] == '1':
                return True  
            else: 
                return False 

    @scale.setter
    def scale(self, value):
        if type(value) is not bool:
            raise TypeError("Only bool value(true/false) supported.")
        cmd = "flogi scale enable"
        if not value:
            cmd = "no "+cmd
        out = self.__swobj.config(cmd)
        if out is not None:
            raise CLIError(cmd, out['msg'])

    # TODO npv