# coding: utf-8

from time import sleep
import random
import subprocess
import logging
from gfhelper.core import screencap
from cStringIO import StringIO
import imagehash
from PIL import Image
import numpy as np

RANDOM_WAIT_MAX = 3500
RANDOM_WAIT_MIN = 2000
STD_WAIT = 4000
FIGHT_WAIT = 12000
SWIPE_OFFSET = 5
PRESS_DURATION = 100
SCROLL_DURATION = 1000

ADB_PATH = "/home/kurefm/Apps/android-sdk/platform-tools/adb"

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


def filter_color(img, color):
    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if not pixels[i, j] == color:
                pixels[i, j] = (0, 0, 0)

    return img


def is_fight_end():
    thash = imagehash.ImageHash(np.array(
        [bool(int(i)) for i in bin(int('d4aaccaeecae8cad4ca944a94ca968a948894a594e9444f464d5649624e62462', 16))[2:]]))
    return (imagehash.dhash(
        filter_color(screencap().convert('RGB'), (255, 255, 255)).crop((37, 40, 280, 100)), 16) - thash) < 10


def wait_fight_end(time=FIGHT_WAIT):
    __logger.info("Wait fight end")
    wait(time)
    while not is_fight_end():
        __logger.error('尚未检测到战斗结算界面')
    random_wait_lite()
    __logger.info("Fight End")


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
