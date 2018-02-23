# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-16 17:47
# author:  kurefm

from functools import wraps
from gfhelper.tools import random_id, reprify
import logging
import re
from datetime import datetime
import inspect


class Func(object):
    def __init__(self, name, *args, **kwargs):
        super(Func, self).__init__()
        self._name = name
        self._args = args if args else []
        self._kwargs = kwargs if kwargs else {}

    @property
    def name(self):
        return self._name

    @property
    def simple_name(self):
        return self._name.split('.')[-1]

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @staticmethod
    def parse(s):
        def unpack(s):
            if s[0] == "'" and s[-1] == "'":
                return s[1:-1]
            elif '.' in s:
                return float(s)
            else:
                return int(s)

        splited = filter(None, re.split(r'\(|\)|\s|,', s))
        name = splited.pop(0)
        splited = map(lambda x: x.split('='), splited)

        args = []
        kwargs = {}
        for item in splited:
            if len(item) == 1:
                args.append(unpack(item[0]))
            elif len(item) == 2:
                kwargs[item[0]] = unpack(item[1])

        return Func(name, *args, **kwargs)

    def __eq__(self, other):
        return isinstance(other, Func) and \
               (self._name == other._name) and \
               (self._args == other._args) and \
               (self._kwargs == other._kwargs)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return '{}({})'.format(
            self.name,
            ', '.join(reprify(list(self.args)) + ['{}={}'.format(k, repr(v)) for k, v in self._kwargs.iteritems()]),
        )


class Trace(Func):
    """
    Trace log object
    """

    def __init__(self, name, *args, **kwargs):
        self._id = kwargs.pop('id', random_id())

        super(Trace, self).__init__(name, *args, **kwargs)

    def __str__(self):
        return self._id + ' | ' + super(Trace, self).__str__()


class Redo(Trace):
    """
    Redo log object
    """

    def __init__(self, name, *args, **kwargs):
        self._start_at = kwargs.pop('start_at', None)
        self._end_at = kwargs.pop('start_at', None)

        super(Redo, self).__init__(name, *args, **kwargs)

    def before_exec_msg(self):
        self._start_at = datetime.now()
        return self._start_at.isoformat() + ' | ' + super(Redo, self).__str__()

    def after_exec_msg(self):
        self._end_at = datetime.now()
        return ' | ' + self._end_at.isoformat()


class Tracer(object):
    def __init__(self, redofile, tracefile):
        self._redofile = redofile if isinstance(redofile, file) else open(redofile, 'a+')
        self._tracefile = tracefile if isinstance(tracefile, file) else open(tracefile, 'a+')
        self._funcs = {}
        self.__interrupt = False
        self.__intracing = False
        self._logger = logging.getLogger(__name__)
        self._cur_redo = None

    def __del__(self):
        # 中断执行，记录trace日志

        self._redofile.close()
        self._tracefile.close()

    @property
    def funcs(self):
        return self._funcs  #TODO make read only

    @property
    def isinterrupt(self):
        return self.__interrupt

    def interrupt(self):
        self.__interrupt = True

    def traceable(self, *dargs, **dkwargs):
        """
        Note: 不支持有返回值的函数，因为可能会被跳过执行
        :param dargs:
        :param dkwargs:
        :return:
        """

        def decorator(f):
            prefix = dkwargs['prefix'] if dkwargs.get('prefix') else inspect.getmodulename(inspect.getfile(f))
            func_name = '.'.join([prefix, f.__name__])
            self._funcs[func_name] = f
            self._logger.info('Register function: {}'.format(func_name))

            @wraps(f)
            def wrapped_func(*args, **kwargs):
                if not self.__interrupt:
                    can_trace = not self.__intracing
                    if can_trace:
                        self.before_exec(func_name, *args, **kwargs)
                        self.__intracing = True

                    f(*args, **kwargs)

                    if can_trace:
                        self.__intracing = False
                        self.after_exec()
                else:
                    self.unexec(func_name, *args, **kwargs)

            return wrapped_func

        return decorator

    def label(self, *dargs, **dkwargs):
        def decorator(f):
            @wraps(f)
            def wrapped_func(*args, **kwargs):
                pass

            return wrapped_func

        return decorator

    def before_exec(self, func_name, *args, **kwargs):
        self._cur_redo = Redo(func_name, *args, **kwargs)
        self._redofile.write(self._cur_redo.before_exec_msg())

    def after_exec(self):
        self._redofile.write(self._cur_redo.after_exec_msg() + '\n')
        self._redofile.flush()

    def unexec(self, func_name, *args, **kwargs):
        self._tracefile.write(str(Trace(func_name, *args, **kwargs)) + '\n')


tracer = Tracer('redo.log', 'trace.log')
