# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-15 22:38
# author:  kurefm

from ConfigParser import ConfigParser, NoSectionError, NoOptionError

WRITEABLE = 1
READONLY = 0


class Section(object):
    def __init__(self, config_parser, section):
        if section not in config_parser.sections():
            raise NoSectionError('No section: %s' % section)
        super(Section, self).__init__()
        self.__dict__['config'] = config_parser
        self.__dict__['section'] = section

    def __getattr__(self, option):
        return self.config.get(self.section, option)

    def __setattr__(self, option, value):
        self.config.set(self.section, option, value)

    def __iter__(self):
        return self.config.options(self.section).__iter__()


class Configuration(ConfigParser):
    def __init__(self, filename):
        ConfigParser.__init__(self)
        self.filename = filename
        self.read(filename)

    def __del__(self):
        self.save()

    def __getattr__(self, section):
        return Section(self, section)

    def __iter__(self):
        return self.sections().__iter__()

    def __dir__(self):
        return dir(ConfigParser) + ['filename', 'save', 'reload']

    def reload(self, filename=None):
        self.read(filename)

    def save(self, filename=None):
        filename = self.filename if not filename else filename

        with open(filename, 'wb') as fp:
            self.write(fp)


class MultiConfig(object):
    def __init__(self, *args):
        self._configs = []
        for filename in args:
            self.append(filename)

    def __del__(self):
        self.save()

    def append(self, filename, flags=WRITEABLE):
        config = ConfigParser()
        config.read(filename)
        # tuple (filename, configparser object, flags)
        self._configs.append((filename, config, flags))

    def save(self):
        for filename, config, flags in self._configs:
            if flags & WRITEABLE:
                with open(filename, 'w') as fp:
                    config.write(fp)

    def get(self, section, option=None, *args):
        if '.' in section:
            section, option = section.split('.')
        for _, config, _ in reversed(self._configs):
            try:
                return config.get(section, option, *args) if option else config.items(section, *args)
            except (NoSectionError, NoOptionError):
                continue
        return None

    def _find_latest_writable(self):
        for _, config, flags in reversed(self._configs):
            if flags & WRITEABLE:
                return config
        return None

    def set(self, section, option, value):
        config = self._find_latest_writable()
        if not config:
            raise ValueError('No a writeable file')

        if not config.has_section(section):
            config.add_section(section)

        config.set(section, option, value)


class Config(object):
    pass
