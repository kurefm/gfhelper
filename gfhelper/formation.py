# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:25
# author:  kurefm

from .app import app
from .tracer import tracer
from .core import tap, screencap
from .cv import check
import logging
from functools import partial
from contextlib import contextmanager

__traceable = tracer.traceable
__inject_args = app.config.inject_args
__logger = logging.getLogger(__name__)


class Rarity(object):
    General = 1 << 1
    Rare = 1 << 2
    Epochal = 1 << 3
    Legendary = 1 << 4
    Extra = 1


class Type(object):
    HG = 1 << 5
    SMG = 1 << 6
    RF = 1 << 7
    AR = 1 << 8
    MG = 1 << 9
    SG = 1 << 10


@__traceable()
@__inject_args()
def enter(params):
    tap(params['region'])
    while not check(screencap(), params['cv_detection']):
        pass


@__traceable()
@__inject_args()
def back(params):
    tap(params['region'])


@contextmanager
def formation():
    enter()
    yield
    back()


@__traceable()
def formation_echelon(no):
    pass


@__traceable()
def change_people(no):
    pass


@__traceable()
def select_people(row, col):
    pass


@__traceable()
def remove_people():
    select_people(1, 1)


@__traceable()
def orderby(flag):
    pass


@__traceable()
def filterby(flags):
    pass
