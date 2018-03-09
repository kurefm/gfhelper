# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-25 11:45
# author:  kurefm

from .app import app
from .cv import has_color, ensure, check
from .core import screencap, tap, wait
import contextlib
import logging

__logger = logging.getLogger(__name__)


def wait_into_factory():
    ensure(screencap, app.config.get('factory.in_factory'), '等待进入工厂界面')
    __logger.info('Current in factory')


def enter():
    tap(app.config.get('factory.enter'))
    wait(500)
    wait_into_factory()


def back():
    tap(app.config.get('factory.back'))
    wait(500)


@contextlib.contextmanager
def factory():
    enter()
    yield
    wait_into_factory()
    back()


def __select_function(no):
    box = app.config.get('factory.function.box_model')
    region = box[no - 1, 0]

    while not has_color(
            screencap().crop(region),
            app.config.get('factory.function.selected_color')
    ):
        tap(region)
        wait(500)


def produce_doll():
    __select_function(1)


def dummy_link():
    __select_function(2)


def doll_powerup():
    __select_function(3)


def retire():
    __select_function(4)


def produce_equip():
    __select_function(5)


def __retire_type(no):
    box = app.config.get('factory.retire.box_model')
    tap(box[0, no - 1])
    wait(500)
    ensure(screencap, app.config.get('factory.in_select'), '等待进入选择界面')


def retire_doll():
    __retire_type(1)


def retire_equip():
    __retire_type(2)


def retire_fairy():
    __retire_type(3)


def read_rarity(img):
    box = app.config.get('factory.star.box_model')
    colors = app.config.get('factory.star.color')
    rarity = 0
    for i in range(5):
        x2, y1, x1, y2 = box[i]
        region = x1, y1, x2, y2
        if has_color(img.crop(region), colors):
            rarity += 1
        else:
            break
    return rarity


def select_all_doll(max_rarity=2):
    retire_doll()
    img = screencap()
    box = app.config.get('factory.select_doll.box_model')
    count = 0
    for row in [1, 2]:
        for col in [1, 2, 3, 4, 5, 6]:
            region = box[row - 1, col - 1]
            if 0 < read_rarity(img.crop(region)) <= max_rarity:
                tap(region)
                count += 1
    tap(app.config.get('factory.select_doll.ack'))
    wait_into_factory()
    return count


def ack_retire():
    tap(app.config.get('factory.retire.ack'))
    wait(500)
    if check(screencap(), app.config.get('factory.retire.warn_dialog.cv_detection')):
        tap(app.config.get('factory.retire.warn_dialog.ack'))
    wait(500)
