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
import subprocess
import time
from functools import partial, wraps
from random import randint
import logging
import re
from cStringIO import StringIO
from PIL import Image

from .app import app
from .tools import *
from .tracer import tracer

_traceable = tracer.traceable
_logger = logging.getLogger(__name__)


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
    return Image.open(StringIO(adb_shell('screencap', '-p').get('stdout')))


@_traceable()
def tap(*region):
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
        point = [
            randint(region[0], region[2]),
            randint(region[1], region[3])
        ]
    else:
        return

    adb_shell(
        'input', 'swipe',
        point[0], point[1], point[0], point[1],
        app.config.get('core.tap_duration')
    )


@_traceable()
def scroll_up(y):
    adb_shell(
        'input', 'swipe',
        960, 200,  # from
        960, 200 + y,  # to
        app.config.get('core.scroll_duration')
    )


@_traceable()
def scroll_down(y):
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

    def run(self):
        self._script()

    def doc(self):
        return ', '.join(
            filter(None, map(str.strip, re.split('\n', self._script.__doc__)))
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
