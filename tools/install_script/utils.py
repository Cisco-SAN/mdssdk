import sys
import pyinputplus as pyinput

# Color
R = "\x1b[38;5;9mHello World\x1b[39;49m"  # Red
G = "\x1b[38;5;10mHello World\x1b[39;49m"  # Green
Y = "\x1b[38;5;11mHello World\x1b[39;49m"  # Yellow
B = "\x1b[38;5;14mHello World\x1b[39;49m"  # Blue
N = "\033[0m"  # Reset


def GREEN(x):
    return G.replace("Hello World", x) + N


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
    return ("{:0>2}h:{:0>2}m:{:05.2f}s".format(int(hours), int(minutes), seconds))


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
    clr_lines(rowlength + 4)
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
