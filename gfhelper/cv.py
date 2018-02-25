# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-21 10:34
# author:  kurefm

import imagehash
import numpy as np
from .tools import *
from .core import wait
from .app import app
import time
import logging

__logger = logging.getLogger(__name__)
__config = app.config.get('cv')


class Color(object):
    def __init__(self, *color):
        if len(color) == 1:
            color = color[0]

        if (isinstance(color, str) or isinstance(color, unicode)) and color.startswith('#'):
            color = [int(color[i: i + 2], 16) for i in (1, 3, 5)]
        elif not islistortuple(color):
            color = 0, 0, 0

        self.r, self.g, self.b = color

    def hex(self):
        return '#%02X%02X%02X' % self.rgb()

    def rgb(self):
        return self.r, self.g, self.b

    def __eq__(self, other):
        return isinstance(other, Color) and self.rgb() == other.rgb()

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return self.hex()


def cmp_hash(first, second, delta=5):
    if isinstance(first, str):
        _hash = int(first, 16)
        first = imagehash.ImageHash(np.array([bool((_hash >> i) & 1) for i in range(64 * 4 - 1, -1, -1)]))
    if isinstance(second, str):
        _hash = int(second, 16)
        second = imagehash.ImageHash(np.array([bool((_hash >> i) & 1) for i in range(64 * 4 - 1, -1, -1)]))

    return first - second <= delta


def filter_color(img, colors):
    colors = [Color(color).rgb() for color in colors]

    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] not in colors:
                pixels[i, j] = (0, 0, 0)

    return img


def __check(img, params):
    if params.crop:
        img = img.crop(params.crop)

    if params.filter:
        filter_color(img, params.filter)

    return cmp_hash(getattr(imagehash, params.hash_type)(img, params.hash_size), params.imghash, params.delta)


def check(img, params):
    for p in params:
        if not __check(img, p):
            return False
    return True


def ensure(img_func, params, msg=None, duration=__config['ensure_duration']):
    while not check(img_func(), params):
        wait(duration)
        if msg: __logger.warning(msg)


def has_color(img, colors):
    colors = [Color(color).rgb() for color in colors]

    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i, j] in colors:
                return True
    return


def ensure_color(img_func, colors, msg=None, duration=__config['ensure_duration'], ):
    while not has_color(img_func(), colors):
        wait(duration)
        if msg: __logger.warning(msg)


def ensure_not_color(img_func, colors, msg=None, duration=__config['ensure_duration']):
    while has_color(img_func(), colors):
        wait(duration)
        if msg: __logger.warning(msg)
