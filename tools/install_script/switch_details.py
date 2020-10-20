import logging
import re
import time
import tools.install_script.utils as utils
import threading

log = logging.getLogger(__name__)


class SwitchDetails(object):

    def __init__(self, ip, swobj):
        self.ip = ip
        self.swobj = swobj

        self.start_time = time.time()
        self.e_time = int(time.time() - self.start_time)

    @property
    def elapsed_time(self):
        # if "Install has been successful" in self.install_status:
        #     self.e_time
        # else:
        #     self.e_time = utils.timeelaped(self.start_time,time.time())
        # return self.e_time
        if self.t.is_alive():
            self.e_time = utils.timeelaped(self.start_time, time.time())
        else:
            self.e_time
        return self.e_time

    def get_cmd_output(self, cmd, only_npv=False, only_npiv=False):
        if only_npv:
            if self.swobj.npv:
                out = self.swobj.show(cmd, raw_text=True)
            else:
                out = ""
        elif only_npiv:
            if self.swobj.npv:
                out = ""
            else:
                out = self.swobj.show(cmd, raw_text=True)
        else:
            out = self.swobj.show(cmd, raw_text=True)
        return out

    def set_thread_basic_info(self):
        self.t = threading.Thread(target=self.collect_basic_info, args=())
        # self.t = utils.PropagatingThread(target=self.collect_basic_info, args=())
        self.t.start()
        # return self.t

    def set_thread_get_upg_img_status(self, upgver):
        self.start_time = time.time()
        self.t = threading.Thread(target=self.get_upg_img_status, args=(upgver,))
        # self.t = utils.PropagatingThread(target=self.get_upg_img_status, args=(upgver,))
        self.t.start()

    def set_thread_to_start_upgrade(self, timeout=1800):
        self.start_time = time.time()
        try:
            self.t = threading.Thread(target=self.start_install, args=(timeout,))
            self.t.start()
        except Exception as e:
            log.debug(e, exc_info=True)
        # self.t = utils.PropagatingThread(target=self.start_install, args=(timeout,))
        # self.t = utils.ExcThread(bucket,target=self.start_install, args=(timeout,))

    def start_install(self, timeout=1800):
        log.debug("Starting install...")
        self.start_time = time.time()
        self.install_status = utils.BLUE("Install Starting..")
        if self.swobj.issu(self.kickupgimg, self.sysupgimg, timeout=timeout):
            count = 1
            while count <= timeout:
                try:
                    tmp = self.swobj.get_install_all_status()
                    log.info(tmp)
                except Exception as e:
                    log.debug(e, exc_info=True)
                if "Install has been successful" in tmp:
                    self.install_status = utils.GREEN(tmp)
                    break
                elif any(ext in tmp for ext in utils.ALL_FAILURES):
                    self.install_status = utils.RED(tmp)
                    break
                else:
                    self.install_status = utils.BLUE(tmp)
                log.debug("CURR STATE: " + self.install_status + " " + str(count))
                count = count + 1
                time.sleep(1)
            log.debug("--------------------- VERSION is " + self.swobj.version)

    def collect_basic_info(self):
        self.ver = self.swobj.version
        self.npv = self.swobj.npv
        n = self.swobj.name
        self.name = re.sub(r'\..*', '', n)
        self.model = self.swobj.model
        self.imgstr = self.swobj.image_string
        self.retstr = utils.BLUE("Checking if upgrade is possible..Please Wait..")
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
        ver_format = self.ver.replace('(', '.').replace(')', '')
        upgver_format = upgver.replace('(', '.').replace(')', '')
        if ver_format == upgver_format:
            self.retstr = utils.RED("Switch version is same as the upgrade version - " + upgver + ".")
            return False
        return True

    def is_img_present(self, upgver):
        self.retstr = utils.BLUE("Checking if upgrade images are present in the switch..Please Wait..")
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
        self.retstr = utils.BLUE("Checking for incompatibilities..Please Wait..")
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
        self.retstr = utils.BLUE("Checking if non-disruptive upgrade is possible..Please Wait..")
        cmd = "show install all impact kickstart " + self.kickupgimg + " system " + self.sysupgimg
        out = self.swobj.show(cmd, raw_text=True, timeout=1000)
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
