# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:24
# author:  kurefm

from .core import _traceable
from functools import partial

traceable = partial(_traceable, profile=__name__)


@traceable()
def select_battle(name):
    pass


@traceable()
def normal_battle():
    pass


@traceable()
def select_echelon(no, count):
    pass


@traceable()
def ack_deploy():
    pass


@traceable()
def start_battle():
    pass


@traceable()
def supply():
    pass


@traceable()
def end_fight(times=4):
    pass


@traceable()
def end_round():
    pass


@traceable()
def end_battle():
    pass


@traceable
def use_fairy_kill():
    pass


@traceable()
def toggle_auto_fairy_skill():
    pass


@traceable()
def toggle_auto_skill():
    pass
