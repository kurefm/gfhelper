# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-25 14:11
# author:  kurefm

"""
主界面相关的操作
"""

from .app import app
from .tracer import tracer
from .core import tap, tap_center, screencap, wait
from . import cv
import logging

__traceable = tracer.traceable
__logger = logging.getLogger(__name__)


@__traceable()
def ensure_enter_game():
    pass


@__traceable()
def wait_into_mainframe(max_times=2):
    """
    等待进入主界面
    """
    times = 0
    while True:
        __logger.info('等待进入主界面')
        img = screencap()
        if cv.check(img, app.config.get('mainframe.in_mainframe')):
            tap_center()
            times += 1
            if times >= max_times: return
        else:
            times = 0
            if cv.check(img, app.config.get('mainframe.in_logistics_dialog')):
                tap(app.config.get('mainframe.continue'))
                __logger.info('继续后勤')
            else:
                tap_center()
        wait(500)
