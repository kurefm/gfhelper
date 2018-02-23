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
from .core import manager, screencap
from .cv import filter_color
from .tracer import tracer
from . import formation
import imagehash

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
    Display info
    """
    click.echo()
    click.echo('  current use: {}'.format(app.config.get('core.current_script')))
    for f_name in tracer.funcs.keys():
        click.echo(f_name)
    click.echo()


@cli.command()
def list():
    """
    List all usable scripts
    """
    click.echo()
    for name, script in manager.scripts.items():
        click.echo('  {:8} {}'.format(name, script.doc()))
    click.echo()


@cli.command()
@click.argument('name', required=True)
def use(name):
    """
    Use script
    """
    app.config.set('core.current_script', name)
    app.config.save()


@cli.command()
def run():
    """
    Run script
    """
    manager.get(app.config.get('core.current_script')).run()


@cli.command()
def test():
    """
    Developer test
    """
    formation.enter()
    formation.back()


@cli.command('cv:test')
@click.argument('config_path')
@click.option('--hash_size', '-s', default=16)
def cv_test(config_path, hash_size):
    params = app.config.get(config_path + '.cv_detection')[0]
    img = screencap()

    img = img.convert('RGB')
    if params.crop:
        img = img.crop(params.crop)

    if params.filter:
        filter_color(img, params.filter)

    img.show()

    hash = getattr(imagehash, params.hash_type)(img, hash_size)
    _logger.info('CV detector hash: %s' % hash)
    if params.hash:
        _logger.info('Delta: %d' % (params.imghash - hash))
