# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-15 22:38
# author:  kurefm

from ruamel import yaml
from ruamel.yaml.comments import CommentedMap
from .cv import CvDetectionParams
from .tools import islistortuple
import functools
import inspect
import logging


class YAMLConfig(object):
    WRITEABLE = 1
    READONLY = 0

    def __init__(self):
        self._raw_configs = []
        self._yaml = yaml.YAML()
        self._yaml.register_class(CvDetectionParams)
        self._logger = logging.getLogger(__name__)

    def append(self, filename, flags=WRITEABLE):
        fp, raw_config = None, None
        try:
            fp = open(filename)
            raw_config = self._yaml.load(fp)
        except IOError:
            pass
        finally:
            fp.close()
            self._raw_configs.append((
                filename,  # filename
                raw_config if raw_config else CommentedMap(),  # config content(nested dict)
                flags  # flags
            ))
            self._logger.info('Load config file: %s' % filename)

    def get(self, key):
        keys = key.split('.')
        for _, config, _ in reversed(self._raw_configs):
            for k in keys:
                config = config.get(k)
                if not config: break
            if config: return config

    def _find_latest_writable(self):
        for _, config, flags in reversed(self._raw_configs):
            if flags & YAMLConfig.WRITEABLE:
                return config
        return None

    def set(self, key, value):
        config = self._find_latest_writable()
        if config is None:
            raise ValueError('No a writeable file')
        ks = key.split('.')
        lk = ks.pop()
        for k in ks:
            if config.has_key(k):
                if not isinstance(config.get(k), CommentedMap):
                    raise ValueError('Not allow set %s to %s' % (key, value))
            else:
                config[k] = CommentedMap()
            config = config.get(k)
        config[lk] = value

    def save(self):
        for filename, config, flags in self._raw_configs:
            if flags & YAMLConfig.WRITEABLE:
                with open(filename, 'w') as fp:
                    self._yaml.dump(config, fp)

    def inject_args(self, *name):

        def decorator(f):
            keys = name if name else \
                ['.'.join([inspect.getmodulename(inspect.getfile(f)), f.__name__])]

            @functools.wraps(f)
            def wrapped_func():
                params = map(self.get, keys)

                return f(*params)

            return wrapped_func

        return decorator
