# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-28 12:11
# author:  kurefm

"""
config, initialize, launch app
"""

import os
import click
from gfhelper import config
import logging
from logging.config import fileConfig
from glob import glob


def resolve_path(path, *paths):
    return os.path.realpath(os.path.join(path, *paths))


class App(object):
    def __init__(self, cwd, app_dir, ext_dir):
        self._cwd = cwd
        self._app_dir = app_dir
        self._ext_dir = ext_dir
        self._config = None

    @property
    def config(self):
        return self._config

    def get_cwd_path(self, path='.'):
        return resolve_path(self._cwd, path)

    def get_app_path(self, path='.'):
        return resolve_path(self._app_dir, path)

    def get_ext_path(self, path='.'):
        return resolve_path(self._ext_dir, path)

    def prepare(self):
        # init logger
        fileConfig('logging.ini')

        logger = logging.getLogger(__name__)
        logger.info("========== START ==========")

        # check ext dir
        if not os.path.exists(self._ext_dir):
            logger.debug("External directory not exists, will create it")
            os.mkdir(self._ext_dir)

    def setup(self):
        self.prepare()
        self._config = config.YAMLConfig()

        for filename in glob(self.get_app_path('yaml.d/*.yaml')):
            self._config.append(filename, flags=config.YAMLConfig.READONLY)

        for filename in glob(self.get_app_path('gfhelper/script/*.yaml')):
            self._config.append(filename, flags=config.YAMLConfig.READONLY)

        self._config.append(self.get_ext_path('config.yaml'))

        # log config

    def launch(self):
        import script  # load script
        from .cli import cli as enter_point
        enter_point()


app = App(
    os.getcwd(),
    os.path.dirname(resolve_path(__file__, '..')),
    click.get_app_dir('gfhelper')
)


def main():
    app.setup()
    app.launch()
