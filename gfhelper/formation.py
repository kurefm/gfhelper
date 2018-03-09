# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:25
# author:  kurefm

from .app import app
from .tracer import tracer
from .core import tap, screencap, wait
from . import cv
import logging
from contextlib import contextmanager

__traceable = tracer.traceable
__inject_args = app.config.inject_args
__logger = logging.getLogger(__name__)


class Rarity(object):
    Legendary = ('rarity', 0, 0)
    Epochal = ('rarity', 0, 1)
    Rare = ('rarity', 0, 2)
    General = ('rarity', 1, 0)
    Extra = ('rarity', 1, 1)


class Type(object):
    HG = ('type', 0, 0)
    SMG = ('type', 0, 1)
    RF = ('type', 0, 2)
    AR = ('type', 1, 0)
    MG = ('type', 1, 1)
    SG = ('type', 1, 2)


class Order(object):
    Level = 0
    Rarity = 1
    AcquireSequence = 2
    ID = 3
    Favor = 4
    Damage = 5


@__traceable('formation')
@__inject_args()
def enter(config):
    tap(config['region'])
    wait(500)
    cv.ensure(screencap, config['cv_detection'], '等待进入队伍编成界面')


@__traceable('formation')
@__inject_args()
def back(region):
    tap(region)
    wait(500)


@contextmanager
def formation():
    enter()
    yield
    back()


@__traceable()
def select_echelon(no):
    box = app.config.get('formation.select_echelon.box_model')
    region = box[no - 1, 0]

    while not cv.has_color(
            screencap().crop(region),
            app.config.get('formation.select_echelon.selected_color')
    ):
        tap(region)
        wait(500)


@__traceable()
def change_doll(no):
    box = app.config.get('formation.change_people.box_model')
    tap(box[no - 1])
    wait(500)
    cv.ensure(screencap, app.config.get('formation.change_people.cv_detection'), '等待进入人形选择界面')


@__traceable()
def select_doll(row, col):
    box = app.config.get('formation.select_people.box_model')
    tap(box[row - 1, col - 1])
    wait(500)
    while cv.check(screencap(), app.config.get('formation.change_people.cv_detection')):
        tap(box[row - 1, col - 1])
        wait(500)
    cv.ensure(screencap, app.config.get('formation.enter.cv_detection'), '等待进入队伍编成界面')


@__traceable()
def remove_people(no):
    change_doll(no)
    select_doll(1, 1)


@__traceable()
def orderby(flag):
    box = app.config.get('formation.orderby.box_model')
    tap(app.config.get('formation.orderby.open'))
    tap(box[flag, 0])
    wait(500)  # wait sort finish


@__traceable()
def filterby(*flags):
    rarity = app.config.get('formation.filterby.rarity')
    type = app.config.get('formation.filterby.type')

    tap(app.config.get('formation.filterby.open'))
    wait(100)
    for flag in flags:
        if flag[0] == 'type':
            tap(type[flag[1:]])
        if flag[0] == 'rarity':
            tap(rarity[flag[1:]])

    tap(app.config.get('formation.filterby.ack'))
    wait(500)


@__traceable('formation')
@__inject_args('formation.filterby')
def reset_filter(config):
    tap(config['open'])
    wait(100)
    tap(config['reset'])
    wait(500)
