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
import config
import logging
from logging.config import fileConfig
from glob import glob
import imp
import ast
import timeit
import traceback
import sys


def resolve_path(path, *paths):
    return os.path.realpath(os.path.join(path, *paths))


class App(object):
    def __init__(self, cwd, app_dir, ext_dir):
        self._start_at = timeit.default_timer()
        self._cwd = cwd
        self._app_dir = app_dir
        self._ext_dir = ext_dir
        self._config = None
        self._logger = None
        self._script = {}

    @property
    def config(self):
        return self._config

    @property
    def scripts(self):
        return self._script

    def get_cwd_path(self, path='.'):
        return resolve_path(self._cwd, path)

    def get_app_path(self, path='.'):
        return resolve_path(self._app_dir, path)

    def get_ext_path(self, path='.'):
        return resolve_path(self._ext_dir, path)

    def search_script(self, path):
        self._logger.debug('Search script on path %s' % path)
        for path in glob(os.path.join(path, '*.py')):
            name = os.path.splitext(os.path.basename(path))[0]
            if name == '__init__': continue
            with open(path) as fp:
                doc = ast.get_docstring(ast.parse(fp.read()))
            self._logger.info('Find script %s(%s)' % (name, doc))
            self._script[name] = (path, doc or '')

    def prepare(self):
        # init logger
        fileConfig('logging.ini')

        self._logger = logging.getLogger(__name__)
        self._logger.info('========== START ==========')

        # check ext dir
        if not os.path.exists(self._ext_dir):
            self._logger.debug("External directory not exists, will create it")
            os.mkdir(self._ext_dir)

    def setup(self):
        self.prepare()
        self._config = config.YAMLConfig()

        for filename in glob(self.get_app_path('yaml.d/*.yaml')):
            self._config.append(filename, flags=config.YAMLConfig.READONLY)

        for filename in glob(self.get_app_path('gfhelper/script/*.yaml')):
            self._config.append(filename, flags=config.YAMLConfig.READONLY)

        self._config.append(self.get_ext_path('config.yaml'))

    def launch(self):
        self.search_script(self.get_app_path('gfhelper/script'))
        script_name = self.config.get('core.current_script')
        if script_name:
            try:
                imp.load_source(script_name, self.scripts[script_name][0])
            except Exception:
                pass

        from .cli import cli as entry_point
        from .tracer import tracer
        try:
            entry_point(standalone_mode=False)
        except click.Abort:
            click.echo('Aborted!', file=sys.stderr)
            sys.exit(1)
        except Exception:
            click.echo(traceback.format_exc(), file=sys.stderr)
        finally:
            self._logger.info('Program run time: %.2fs' % (timeit.default_timer() - self._start_at))
            self._logger.info('==========  END  ==========')


app = App(
    os.getcwd(),
    os.path.dirname(resolve_path(__file__, '..')),
    click.get_app_dir('gfhelper')
)
