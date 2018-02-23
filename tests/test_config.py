# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-15 22:56
# author:  kurefm

from unittest import TestCase
from gfhelper import config
import ruamel.yaml
import sys


class ConditionParams(object):
    def __init__(self, thash, hash_type, crop, filter, delta):
        self.thash = thash
        self.hash_type = hash_type
        self.crop = crop
        self.filter = filter
        self.delta = delta

    @property
    def hash_size(self):
        return len(self.thash) / 4


class TestYAMLConfig(TestCase):
    def setUp(self):
        self.config = config.YAMLConfig()
        self.config.append('tests/resources/readonly.yaml', config.READONLY)
        self.config.append('tests/resources/writeable.yaml')

    def test_read_config(self):
        self.assertEqual(self.config.get('gfhelper.core.network_delay'), 4001)
        self.assertEqual(self.config.get('gfhelper.core.load_delay'), 1500)
        self.assertListEqual(self.config.get('gfhelper.formation.region.enter'), [121, 121, 121, 121])
        self.assertListEqual(self.config.get('gfhelper.formation.region.back'), [13, 13, 13, 13])
        self.assertIsInstance(self.config.get('gfhelper.core'), dict)

    def test_write_config(self):
        self.assertIsNone(self.config.get('gfhelper.core.current_use'))
        self.config.set('gfhelper.core.current_use', 'script')
        self.config.save()
        self.assertIsNotNone(self.config.get('gfhelper.core.current_use'))
        self.config.set('gfhelper.core.current_use', None)
        self.config.save()

    def test_dump_object(self):
        params = ConditionParams(
            '123',
            'dhash',
            (190, 90, 290, 190),
            ['#FFFFFF', '#343434'],
            10
        )
        yaml = ruamel.yaml.YAML()
        yaml.register_class(ConditionParams)
        yaml.dump({
            'formation': {
                'enter': {
                    'check': [params]
                }
            }
        }, sys.stdout)

    def test_inject_args(self):
        @self.config.inject_args()
        def test_func1(arg1):
            self.assertEquals(arg1, 1)

        @self.config.inject_args('gfhelper.core.network_delay')
        def test_func2(network_delay):
            self.assertEquals(network_delay, 4001)

        @self.config.inject_args(
            'gfhelper.core.network_delay',
            'gfhelper.core.scroll_duration'
        )
        def test_func2(network_delay, scroll_duration):
            self.assertEquals(network_delay, 4001)
            self.assertEquals(scroll_duration, 501)

        test_func1()
        test_func2()
