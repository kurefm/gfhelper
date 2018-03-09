# coding: utf-8

from functools import partial
import os


def islistortuple(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)


def someify(any, op):
    if isinstance(any, list):
        return map(op, any)
    elif isinstance(any, tuple):
        return tuple(map(op, any))
    elif isinstance(any, dict):
        return {k: op(v) for k, v in any.iteritems()}
    else:
        return op(any)


strify = partial(someify, op=str)

reprify = partial(someify, op=repr)


def random_id(n=4):
    return ''.join("{:02x}".format(ord(c)) for c in os.urandom(n))
