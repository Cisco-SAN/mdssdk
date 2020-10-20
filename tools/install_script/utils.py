import sys
import pyinputplus as pyinput
from threading import Thread


class PropagatingThread(Thread):
    def run(self):
        self.exc = None
        try:
            if hasattr(self, '_Thread__target'):
                # Thread uses name mangling prior to Python 3.
                self.ret = self._Thread__target(*self._Thread__args, **self._Thread__kwargs)
            else:
                self.ret = self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self.exc = e

    def join(self, timeout):
        super(PropagatingThread, self).join(timeout=timeout)
        if self.exc:
            raise self.exc
        return self.ret


# Color
R = "\x1b[38;5;9mHello World\x1b[39;49m"  # Red
G = "\x1b[38;5;10mHello World\x1b[39;49m"  # Green
Y = "\x1b[38;5;11mHello World\x1b[39;49m"  # Yellow
B = "\x1b[38;5;14mHello World\x1b[39;49m"  # Blue
N = "\033[0m"  # Reset

ALL_FAILURES = ['fail', 'FAIL']


def GREEN(x):
    return G.replace("Hello World", x) + N


def BLUE(x):
    return B.replace("Hello World", x) + N


def RED(x):
    return R.replace("Hello World", x) + N


def banner(text, ch='-', length=78):
    spaced_text = '   %s   ' % text
    banner = spaced_text.center(length, ch)
    print()
    print(ch * length)
    print(banner)
    print(ch * length)
    print()


def timeelaped(start, end):
    hours, rem = divmod(end - start, 3600)
    minutes, seconds = divmod(rem, 60)
    return ("{:0>1}h:{:0>1}m:{:02.1f}s".format(int(hours), int(minutes), seconds))


def get_kick_sys_img_string(upgimg, imgstr):
    if imgstr is None:
        return None, None
    upgimg_mod = upgimg.replace('(', '.').replace(')', '')
    kick = imgstr + '-kickstart-mz.' + upgimg_mod + '.bin'
    syst = imgstr + '-mz.' + upgimg_mod + '.bin'
    return kick, syst


def is_image_present(sw, img):
    if img is not None:
        cmd = "dir " + img
        out = sw.show(cmd)
        if 'No such file or directory' in out:
            return False
        return True


def clr_lines(num_of_lines):
    for _ in range(num_of_lines):
        sys.stdout.write("\x1b[1A")
        sys.stdout.write("\x1b[2K")


def print_table_in_same_place(rowlength, x):
    clr_lines(rowlength + 6)
    print(x)


def askIP():
    r = pyinput.inputIP("Enter seed switch ip address: ")
    return r


def askUser():
    r = pyinput.inputStr("Username: ")
    return r


def askPassword():
    r = pyinput.inputPassword("Password: ")
    return r


def askNPV():
    r = pyinput.inputYesNo("Discover NPV (yes/no)? [yes] ", blank=True)
    if r == '' or r == 'yes':
        return True
    else:
        return False


def askVersionUpgrade():
    r = pyinput.inputStr("Upgrade to version : ")
    return r


def askForPrePostCheck():
    r = pyinput.inputYesNo(
        "Do you want to do post ISSU checks for components present in 'checks.json' file (yes/no)? [yes] ", blank=True)
    if r == '' or r == 'yes':
        return True
    else:
        return False
