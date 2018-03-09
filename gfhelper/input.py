# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-25 15:46
# author:  kurefm

"""
Android input touch event, only work on type B device

About mt protocol see https://tinylab.gitbooks.io/linux-doc/zh-cn/input/multi-touch-protocol.html
About const defined see https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
"""

from gfhelper.core import adb_shell, wait
from gfhelper.app import app
import random

# Event types

EV_SYN = 0x00
EV_KEY = 0x01
EV_ABS = 0x03

# Synchronization events

SYN_REPORT = 0
SYN_CONFIG = 1
SYN_MT_REPORT = 2
SYN_DROPPED = 3
SYN_MAX = 0xf
SYN_CNT = (SYN_MAX + 1)

# Absolute axes
ABS_MT_SLOT = 0x2f  # MT slot being modified
ABS_MT_TOUCH_MAJOR = 0x30  # Major axis of touching ellipse
ABS_MT_TOUCH_MINOR = 0x31  # Minor axis (omit if circular)
ABS_MT_POSITION_X = 0x35  # Center X touch position
ABS_MT_POSITION_Y = 0x36  # Center Y touch position
ABS_MT_TRACKING_ID = 0x39  # Unique ID of initiated contact

BTN_TOOL_FINGER = 0x145

# Event values

UP = 0
DOWN = 1


class InputManger(object):
    class Slot(object):
        def __init__(self, slot, inputmanger):
            self.slot = slot
            self._inputmanger = inputmanger
            self._freed = False

        def touch(self, x, y):
            self._inputmanger.mt_touch(self.slot, x, y)

        def free(self):
            self._inputmanger.free_slot(self.slot)
            self._freed = True

    def __init__(self, device):
        self.used_slot = []
        self.max_slot = 9
        self.max_tracking_id = 65535
        self.device = device

    def sendevent(self, type, code, value):
        adb_shell('sendevent', self.device, type, code, value)

    def tracking_id(self):
        return random.randint(0, self.max_tracking_id)

    def mt_touch(self, slot, x, y):
        self.sendevent(EV_ABS, ABS_MT_SLOT, slot)
        self.sendevent(EV_ABS, ABS_MT_POSITION_X, x)
        self.sendevent(EV_ABS, ABS_MT_POSITION_Y, y)
        self.sendevent(EV_SYN, SYN_REPORT, 0)

    def touch(self, x, y, duration):
        self.sendevent(EV_ABS, ABS_MT_TRACKING_ID, self.tracking_id())
        self.sendevent(EV_KEY, BTN_TOOL_FINGER, DOWN)
        self.sendevent(EV_ABS, ABS_MT_POSITION_X, x)
        self.sendevent(EV_ABS, ABS_MT_POSITION_Y, y)
        self.sendevent(EV_SYN, SYN_REPORT, 0)
        wait(duration)
        self.sendevent(EV_ABS, ABS_MT_TRACKING_ID, 0xffffffff)
        self.sendevent(EV_KEY, BTN_TOOL_FINGER, UP)
        self.sendevent(EV_SYN, SYN_REPORT, 0)

    def new_slot(self, x, y):
        slot = 0
        for i in sorted(self.used_slot):
            if i == slot: slot += 1

        self.sendevent(EV_ABS, ABS_MT_SLOT, slot)
        self.sendevent(EV_ABS, ABS_MT_TRACKING_ID, self.tracking_id())

        # if used slot is empty, means that is first slot
        if not self.used_slot:
            self.sendevent(EV_KEY, BTN_TOOL_FINGER, DOWN)

        self.sendevent(EV_ABS, ABS_MT_POSITION_X, x)
        self.sendevent(EV_ABS, ABS_MT_POSITION_Y, y)

        self.sendevent(EV_SYN, SYN_REPORT, 0)

        self.used_slot.append(slot)
        return InputManger.Slot(slot, self)

    def free_slot(self, slot):
        self.sendevent(EV_ABS, ABS_MT_SLOT, slot)
        self.sendevent(EV_ABS, ABS_MT_TRACKING_ID, 0xffffffff)
        # if used list is empty, mean that is the last slot
        if not self.used_slot:
            self.sendevent(EV_KEY, BTN_TOOL_FINGER, UP)
        self.sendevent(EV_SYN, SYN_REPORT, 0)
        self.used_slot.remove(slot)


inputmanger = InputManger(app.config.get('core.input.device'))
