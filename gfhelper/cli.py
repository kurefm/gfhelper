# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-24 14:11
# author:  kurefm

from __future__ import division
import click
import time
import random
from .app import app
from .core import manager
from functools import partial

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
    app.config.set('core', 'current_script', name)
    app.config.save()


@cli.command()
def run():
    """
    Run script
    """
    manager.get(app.config.get('core.current_script')).run()
