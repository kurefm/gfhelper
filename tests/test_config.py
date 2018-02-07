# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-15 22:56
# author:  kurefm

from unittest import TestCase
from ConfigParser import ConfigParser
from gfhelper import config


class TestReadConfigOriginal(TestCase):
    def setUp(self):
        self.config = ConfigParser()
        self.config.read('tests/resources/config.ini')

    def test_check_config(self):
        self.assertEqual(self.config.get('session1', 'key1'), 'value1')

    def tearDown(self):
        self.config = None


class TestReadConfig(TestCase):
    def setUp(self):
        self.config = config.Configuration('tests/resources/config.ini')

    def test_check_config(self):
        self.assertEqual(self.config.session1.key1, 'value1')

    def tearDown(self):
        self.config = None


class TestMultiConfig(TestCase):
    def setUp(self):
        self.config = config.MultiConfig()
        self.config.append('tests/resources/readonly.ini', config.READONLY)
        self.config.append('tests/resources/writeable.ini', config.WRITEABLE)

    def test_read_config(self):
        self.assertEqual(self.config.get('section1.key1'), 'value1')
        self.assertEqual(self.config.get('section2.key2'), 'value2')
        self.assertEqual(self.config.get('section3.key3'), 'value3')
        self.assertEqual(self.config.get('section4.key4'), 'value44')
        self.assertEqual(self.config.get('section5.key1'), 'value51')

