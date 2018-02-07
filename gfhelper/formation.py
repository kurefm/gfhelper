# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:25
# author:  kurefm

from functools import partial
from contextlib import contextmanager
from .tracer import tracer

_traceable = partial(tracer.traceable, prefix=__name__)


@_traceable()
def enter():
    pass


@_traceable()
def back():
    pass


@contextmanager
def formation():
    enter()
    yield
    back()


@_traceable()
def formation_echelon(no):
    pass


@_traceable()
def change_people(no):
    pass


@_traceable()
def select_people(row, col):
    pass


@_traceable()
def remove_people():
    select_people(1, 1)


@_traceable()
def orderby(flag):
    pass


@_traceable()
def filterby(flags):
    pass
