# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-27 15:50
# author:  kurefm

from .app import app
from .core import wait, tap, screencap
from cv import ensure
import logging
import contextlib

__logger = logging.getLogger(__name__)


def wait_into_restore():
    ensure(screencap, app.config.get('restore.in_restore'), '等待进入修复界面')
    __logger.info('Current in restore')


def enter():
    tap(app.config.get('restore.enter'))
    wait(500)
    wait_into_restore()


def back():
    tap(app.config.get('restore.back'))
    wait(500)


@contextlib.contextmanager
def restore():
    enter()
    yield
    wait_into_restore()
    back()


def select_slot(no):
    box = app.config.get('restore.select_slot')
    tap(box[no - 1])
    __logger.info('Select No.%s restore slot' % no)
    ensure(screencap, app.config.get('restore.in_doll_select'), '等待进入选择人形界面')


def select_doll(row, col):
    box = app.config.get('restore.select_doll')
    tap(box[row - 1, col - 1])


def ack_restore(quick=False):
    tap(app.config.get('restore.ack'))
    ensure(screencap, app.config.get('restore.restore_dialog.cv_detection'), '等待进入修复对话框')
    if quick:
        tap(app.config.get('restore.restore_dialog.quick'))
    tap(app.config.get('restore.restore_dialog.ack'))
    if quick:
        ensure(screencap, app.config.get('restore.finish_dialog.cv_detection'), '等待进入修复完成对话框')
        tap(app.config.get('restore.finish_dialog.close'))
