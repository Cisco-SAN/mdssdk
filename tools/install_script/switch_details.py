import logging
import re
import time
import random

log = logging.getLogger(__name__)
import utils
import threading


class SwitchDetails(object):

    def __init__(self, ip, swobj):
        self.ip = ip
        self.swobj = swobj

    def get_cmd_output(self, cmd):
        out = self.swobj.show(cmd, raw_text=True)
        return out

    def set_thread_basic_info(self):
        self.t = threading.Thread(target=self.collect_basic_info, args=())
        return self.t

    def set_thread_get_upg_img_status(self, upgver):
        self.t = threading.Thread(target=self.get_upg_img_status, args=(upgver,))
        return self.t

    def collect_basic_info(self):
        self.ver = self.swobj.version
        self.npv = self.swobj.npv
        n = self.swobj.name
        self.name = re.sub(r'\..*', '', n)
        self.model = self.swobj.model
        self.imgstr = self.swobj.image_string
        self.retstr = "Checking if upgrade is possible..Please Wait.."
        self.done_upgrade_checks = False
        self.can_upgrade = False

    def get_upg_img_status(self, upgver):
        if self.is_upgrade_required(upgver):
            if self.imgstr is None:
                self.kickupgimg = None
                self.sysupgimg = None
                self.retstr = utils.RED("Could not form image name from image string. Please check log file.")
                log.debug(self.retstr)
            else:
                self.kickupgimg, self.sysupgimg = utils.get_kick_sys_img_string(upgver, self.imgstr)
                if self.is_img_present(upgver):
                    if self._is_incompatibile():
                        self.retstr = utils.RED("Incompatible configurations found.")
                    elif self._check_imapact_status():
                        self.retstr = utils.RED("Upgrade to " + upgver + " is disruptive.")
                    else:
                        self.retstr = utils.GREEN("Ready for non-disruptive upgrade to " + upgver + ".")
                        self.can_upgrade = True
        self.done_upgrade_checks = True

    def is_upgrade_required(self, upgver):
        if self.ver == upgver:
            self.retstr = utils.RED("Switch version is same as the upgrade version - " + upgver + ".")
            return False
        return True

    def is_img_present(self, upgver):
        self.retstr = "Checking if upgrade images are present in the switch..Please Wait.."
        kf = utils.is_image_present(self.swobj, self.kickupgimg)
        sf = utils.is_image_present(self.swobj, self.sysupgimg)
        if not kf:
            if not sf:
                self.retstr = utils.RED(upgver + " kickstart and system images are not present in the switch.")
                return False
            else:
                self.retstr = utils.RED(upgver + " kickstart image is not present in the switch.")
                return False
        else:
            if not sf:
                self.retstr = utils.RED(upgver + " system image is not present in the switch.")
                return False
        return True

    def _is_incompatibile(self):
        self.retstr = "Checking for incompatibilities..Please Wait.."
        log.debug("Checking incompatibilty on switch " + self.ip)
        cmd = "show incompatibility-all system " + self.sysupgimg
        # self.swobj.timeout = 1000
        out = self.swobj.show(cmd, raw_text=True, timeout=2800)
        self.incompat = out
        alllines = out.splitlines()
        noincompat = 0
        for eachline in alllines:
            if "No incompatible configurations" in eachline:
                noincompat += 1
        if noincompat != 2:
            log.debug(
                self.ip
                + ": Incompatibilty check failed, please fix the incompatibilities. Skipping upgrade"
            )
            # TODO: get the incompatibilties and store in some varibales
            log.debug(out)
            return True
        else:
            return False

    def _check_imapact_status(self):
        # Check impact status to determine if its disruptive or non-disruptive
        # show install all impact kickstart m9700-sf4ek9-kickstart-mz.8.4.1.bin system m9700-sf4ek9-mz.8.4.1.bin
        log.debug("Checking impact status on switch " + self.ip)
        self.retstr = "Checking if non-disruptive upgrade is possible..Please Wait.."
        cmd = "show install all impact kickstart " + self.kickupgimg + " system " + self.sysupgimg
        out = self.swobj.show(cmd, raw_text=True, timeout=2800)
        self.impact = out
        alllines = out.splitlines()
        nondisruptive = False
        for eachline in alllines:
            if "non-disruptive" in eachline:
                nondisruptive = True
                log.debug(self.ip + ": 'show install all impact' was success, continuing with non-disruptive ISSU ")
                break
        if not nondisruptive:
            log.debug(self.ip + ": ERROR!!! Cannot do non-disruptive upgrade. Skipping upgrade")
            log.debug("_check_imapact_status - True" + self.ip)
            log.debug("Done checking impact status on switch." + self.ip)
            return True
        log.debug("_check_imapact_status - False" + self.ip)
        log.debug("Done checking impact status on switch." + self.ip)
        return False