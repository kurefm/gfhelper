# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-17 12:02
# author:  kurefm

from __future__ import print_function
from unittest import TestCase
from gfhelper.tracer import tracer, Func, Redo
from functools import partial
import random
import sys
import time

traceable = partial(tracer.traceable, prefix=__name__)


@traceable()
def core_func1(x, y):
    time.sleep(0.1)
    print(x, y)


@traceable()
def core_func2(x, y):
    time.sleep(0.1)
    print(x, y)


@traceable()
def comm_func1():
    core_func1(10, 10)
    core_func2(20, 20)


class TestFunc(TestCase):
    def test_str(self):
        f = Func('tests.func', 1, 2, 3, a='1', b=2, c=3)
        self.assertEqual(str(f), "tests.func(1, 2, 3, a='1', c=3, b=2)")

    def test_eq(self):
        self.assertTrue(Func('tests.func', 1, 2, 3, a=1, b=2, c=3) == Func('tests.func', 1, 2, 3, a=1, b=2, c=3))
        self.assertFalse(Func('tests.func', 1, 2, 3, a=1, b=2, c=3) == Func('tests.func1', 1, 2, 3, a=1, b=2, c=3))
        self.assertFalse(Func('tests.func', 1, 2, 3, a=1, b=2, c=3) == Func('tests.func', 1, 2, 4, a=1, b=2, c=3))
        self.assertFalse(Func('tests.func', 1, 2, 3, a=1, b=2, c=3) == Func('tests.func', 1, 2, 3, a=1, b=2, c=4))

    def test_parse(self):
        self.assertTrue(Func('tests.func', 1, 2, 3, a=1, b=2, c=3) == Func.parse('tests.func(1, 2, 3, a=1, c=3, b=2)'))


class TestRedo(TestCase):
    def test_msg(self):
        redo = Redo('tests.func', 1, 2, 3, a='1', b=2, c=3)
        sys.stdout.write(redo.before_exec_msg())
        sys.stdout.write(redo.after_exec_msg())
        sys.stdout.flush()


class TestTracer(TestCase):
    def test_decorator(self):
        for i in range(10):
            if random.randint(0, 1):
                core_func1(100, 200)
            else:
                core_func2(100, 200)

        tracer.interrupt()

        for i in range(10):
            if random.randint(0, 1):
                core_func1(100, 200)
            else:
                core_func2(100, 200)

    def test_inner_trace(self):
        core_func1(10, 10)
        core_func2(20, 20)
        comm_func1()
        core_func2(20, 20)
        core_func1(10, 10)

        tracer.interrupt()

        comm_func1()
