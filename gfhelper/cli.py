# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-24 14:11
# author:  kurefm

from __future__ import division
import click
import time
import random
import logging
from .app import app
from . import core
from . import formation
from .cv import filter_color, check
from .tracer import tracer
import imagehash
import os
import inspect

_logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """\b
      ________ _____.__           .__
     /  _____// ____\  |__   ____ |  | ______   ___________
    /   \  __\   __\|  |  \_/ __ \|  | \____ \_/ __ \_  __ \\
    \    \_\  \  |  |   Y  \  ___/|  |_|  |_> >  ___/|  | \/
     \______  /__|  |___|  /\___  >____/   __/ \___  >__|
            \/           \/     \/     |__|        \/
    """
    pass


@cli.command()
def info():
    """
    [buildin] Display info
    """
    click.echo()
    click.echo('  current use: {}'.format(app.config.get('core.current_script')))
    for f_name in tracer.funcs.keys():
        click.echo(f_name)
    click.echo()


@cli.command()
def game():
    """
    [buildin] Launch girl's frontline
    """
    core.launch_game()


@cli.command()
def list():
    """
    [buildin] List all usable scripts
    """
    click.echo()
    for name, (_, doc) in app.scripts.items():
        click.echo('  {:8} {}'.format(name, doc))
    click.echo()


@cli.command()
@click.argument('name', required=True)
def use(name):
    """
    [buildin] Use script
    """
    app.config.set('core.current_script', name)
    app.config.save()


def command(name=None, cls=None, **attrs):
    def decorator(f):
        prefix = inspect.getmodulename(inspect.getfile(f))
        doc = attrs.get('help') or inspect.getdoc(f)

        if doc:
            attrs['help'] = ('[%s] %s' % (prefix, doc)).decode('utf-8')
        cmd = click.command(':'.join((prefix, name or f.__name__)), cls, **attrs)(f)
        cli.add_command(cmd)
        return cmd

    return decorator
