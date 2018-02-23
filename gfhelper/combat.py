# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:24
# author:  kurefm

from .tracer import tracer
from functools import partial
import re

traceable = partial(tracer.traceable, profile=__name__)


class Difficulty(object):
    Normal = 0b001
    Emergency = 0b010
    Midnight = 0b100


def parse_battle_name(name):
    re.match(r'(\d{0,2})-(\d)(?:[en]*)', name)


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
