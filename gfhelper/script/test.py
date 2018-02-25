# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-23 21:07
# author:  kurefm

"""
Test and developer tools
"""

from gfhelper import cli, cv, formation, core
from gfhelper.app import app
import click
import logging
import imagehash
import os

__logger = logging.getLogger(__name__)


@cli.command()
def test():
    """
    Developer test
    """
    with formation.formation():
        formation.select_echelon(1)
        formation.change_doll(4)
        formation.filterby(formation.Rarity.Legendary, formation.Type.AR)
        formation.select_doll(2, 4)
        formation.select_echelon(2)
        formation.change_doll(1)
        formation.select_doll(2, 3)


@cli.command('cv')
@click.argument('config_path')
@click.option('--hash-size', '-s', default=16)
@click.option('--no-suffix', '-Ns', is_flag=True)
def cv_test(config_path, hash_size, no_suffix):
    img = core.screencap()

    if not no_suffix:
        config_path = config_path + '.cv_detection'

    for params in app.config.get(config_path):
        if params.crop:
            _img = img.crop(params.crop)

        if params.filter:
            cv.filter_color(_img, params.filter)

        _img.show()

        hash = getattr(imagehash, params.hash_type)(_img, hash_size)
        __logger.info('CV detector hash: %s' % hash)
        if params.hash:
            __logger.info('Delta: %d' % (params.imghash - hash))

    if cv.check(img, app.config.get(config_path)):
        __logger.info('Test Passed!')
    else:
        __logger.error('Test Failed!')


@cli.command()
@click.argument('filename', metavar='<filename>', required=False)
@click.option('-c', '--crop', nargs=4, type=int)
@click.option('-f', '--filter', multiple=True, type=str)
def screenshot(filename, crop, filter):
    """
    Take a screenshot
    """
    img = core.screencap()
    if crop:
        img = img.crop(crop)
    if filter:
        cv.filter_color(img, filter)
    if filename:
        dir = app.get_ext_path('screenshot')
        if not os.path.exists(dir):
            os.mkdir(dir)
        filename = os.path.join(dir, filename) + '.png'
        img.save(filename)
    else:
        img.show()
