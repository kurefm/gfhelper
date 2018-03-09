# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-21 11:34
# author:  kurefm

"""
core function:

touch, resize, wait
"""

from __future__ import division, print_function

import inspect
import logging
import re
import subprocess
import time
from cStringIO import StringIO
from random import randint

from PIL import Image

from .app import app
from .tools import *
from .tracer import tracer

_traceable = tracer.traceable
__logger = logging.getLogger(__name__)


def adb_shell(*cmd, **kwargs):
    check_call = kwargs.pop('check_call', True)
    # check_return = kwargs.pop('check_return', False)
    for key in 'args', 'stdout', 'stderr':
        if kwargs.has_key(key):
            raise ValueError('{} argument not allowed, it will be overridden.'.format(key))
    popen = subprocess.Popen(
        (app.config.get('core.adb_path'), 'shell') + strify(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        **kwargs
    )

    stdout, stderr = popen.communicate()

    if check_call and popen.returncode:
        raise subprocess.CalledProcessError(popen.returncode, cmd, stdout)

    return dict(
        returncode=popen.returncode,
        stdout=stdout,
        stderr=stderr
    )


def screencap():
    return Image.open(StringIO(adb_shell('screencap', '-p').get('stdout'))).convert('RGB')


def launch_game():
    adb_shell(
        'am', 'start', '-n',
        app.config.get('core.package') + '/' + app.config.get('core.activity')
    )


def stop_game():
    adb_shell(
        'am', 'force-stop', app.config.get('core.package')
    )


@_traceable()
def tap(*region, **kwargs):
    """
    tap a region:

    - point [x, y]
    - circle [x, y, R]
    - rect [x1, y1, x2, y2]
    :param region:
    :return:
    """
    if len(region) == 1 and islistortuple(region):
        region = region[0]

    if len(region) == 2:
        point = region
    elif len(region) == 3:
        point = region[0:2]
    elif len(region) == 4:
        reserved = app.config.get('core.reserved')
        reserved_x = int((region[2] - region[0]) * reserved / 2)
        reserved_y = int((region[3] - region[1]) * reserved / 2)
        point = [
            randint(region[0] + reserved_x, region[2] - reserved_x),
            randint(region[1] + reserved_y, region[3] - reserved_y)
        ]
    else:
        return

    __logger.debug('Tap (%d, %d)' % tuple(point))

    # adb_shell(
    #     'input', 'swipe',
    #     point[0], point[1], point[0], point[1],
    #     app.config.get('core.tap_duration') + randint(0, 25)
    # )

    from .input import inputmanger

    inputmanger.touch(1080 - point[1], point[0],
                      kwargs.get('duration') or app.config.get('core.tap_duration'))
    wait(app.config.get('core.tap_wait'))


@_traceable()
def tap_center():
    tap(1000, 340, 1225, 640)


@_traceable()
def scroll_up(y):
    __logger.debug('Scroll up %d' % y)
    adb_shell(
        'input', 'swipe',
        960, 200,  # from
        960, 200 + y,  # to
        app.config.get('core.scroll_duration')
    )


@_traceable()
def scroll_down(y):
    __logger.debug('Scroll down %d' % y)
    adb_shell(
        'input', 'swipe',
        960, 750,  # from
        960, 750 - y,  # to
        app.config.get('core.scroll_duration')
    )


@_traceable()
def wait_network(delay=app.config.get('core.network_delay')):
    wait(delay)


@_traceable()
def wait_animation(delay=app.config.get('core.animation_delay')):
    wait(delay)


@_traceable()
def wait_load(delay=app.config.get('core.load_delay')):
    wait(delay)


@_traceable()
def wait(duration):
    min, max = duration, duration

    roll = randint(0, 99)
    if roll < 10:
        min += duration * 0.2
        max += duration * 0.4
    elif 10 <= roll < 30:
        min += duration * 0.1
        max += duration * 0.2
    elif 30 <= roll < 100:
        max += duration * 0.1

    duration = randint(min, max)

    __logger.info('Sleep %dms', duration)
    time.sleep(duration / 1000.0)


class Script(object):
    def __init__(self, script, name=None):
        super(Script, self).__init__()
        if not callable(script):
            raise ValueError('Arguments script should be function.')
        self._script = script
        self._name = name if name else script.__name__

    @property
    def name(self):
        return self._name

    def run(self, options=None):
        self._script(options)

    def doc(self):
        return ', '.join(
            filter(None, map(str.strip, re.split('\n', inspect.getdoc(self._script))))
        )


class ScriptManager(object):
    def __init__(self):
        self._scripts = {}  # map script name to object

    def add(self, name, script):
        self._scripts[name] = script

    def script(self, name=None):
        def decorator(f):
            s = Script(f, name)
            self._scripts[s.name] = s
            s.__doc__ = f.__doc__
            return s

        return decorator

    def get(self, name):
        return self._scripts.get(name)

    @property
    def scripts(self):
        return self._scripts


manager = ScriptManager()

script = manager.script
