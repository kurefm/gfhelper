# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-21 16:34
# author:  kurefm


def decorator1(f):
    print 'run decorator1'

    def wrapped_func():
        return f()

    return f


def decorator2(*args, **kwargs):
    def decorator(f):
        print 'run decorator2'

        def wrapped_func():
            return f()

        return f

    return decorator


@decorator2()
def func2():
    print 'run func2'


@decorator1
def func1():
    print 'run func1'
