# coding: utf-8

from time import sleep
import random
import subprocess
import logging

RANDOM_WAIT_MAX = 3500
RANDOM_WAIT_MIN = 2000
STD_WAIT = 4000
FIGHT_WAIT = 15000
SWIPE_OFFSET = 5
PRESS_DURATION = 100
SCROLL_DURATION = 1000

ADB_PATH = "/home/kurefm/Apps/android/platform-tools/adb"

# R 因子，目标屏幕对1080p的倍数
R = 1

__logger = logging.getLogger(__name__)


def islistortuple(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)


def wait(time):
    sleep(time / 1000.0)


def random_wait():
    """
    用于解决脚本探测和软件卡顿
    """
    __logger.info("Wait a moment")
    wait(random.randrange(RANDOM_WAIT_MIN, RANDOM_WAIT_MAX))


def random_wait_lite(r=5):
    """
    用于解决脚本探测和软件卡顿
    """
    wait(random.randrange(RANDOM_WAIT_MIN / r, RANDOM_WAIT_MAX / r))


def std_wait():
    """
    用于解决网络延迟
    """
    __logger.info("Wait network")
    wait(STD_WAIT)
    random_wait_lite()


def wait_fight_end(time=FIGHT_WAIT):
    __logger.info("Wait fight end")
    wait(time)
    std_wait()
    random_wait()


def swipe_offset():
    return random.randrange(-SWIPE_OFFSET, SWIPE_OFFSET)


def strify(any):
    if islistortuple(any):
        return map(str, any)
    else:
        return str(any)


def resize(any):
    if islistortuple(any):
        return map(lambda x: x * R, any)
    else:
        return any * R


def press(x, y, duration=random.randrange(75, 100)):
    __logger.debug("Press {0}, {1}".format(x, y))
    if duration:
        subprocess.check_call(strify([ADB_PATH, 'shell', 'input', 'swipe',
                                      x, y,
                                      x, y,
                                      duration]))
    else:
        subprocess.check_call(strify([ADB_PATH, 'shell', 'input', 'tap', x, y]))


def press_center():
    press(960, 540, 10)


def scroll_up(y, duration=SCROLL_DURATION):
    subprocess.check_call(strify([ADB_PATH, 'shell', 'input', 'swipe',
                                  960, 300,
                                  960, 300 + y,
                                  duration]))


def scroll_down(y, duration=SCROLL_DURATION):
    subprocess.check_call(strify([ADB_PATH, 'shell', 'input', 'swipe',
                                  960, 900,
                                  960, 900 - y,
                                  duration]))
