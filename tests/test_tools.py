# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-16 15:27
# author:  kurefm

from unittest import TestCase
from gfhelper.tools import islistortuple, strify, random_id


class TestHelperFunc(TestCase):
    def test_islistortuple(self):
        self.assertTrue(islistortuple(()))
        self.assertTrue(islistortuple([]))
        self.assertFalse(islistortuple(1))
        self.assertFalse(islistortuple(1.1))
        self.assertFalse(islistortuple('1'))
        self.assertFalse(islistortuple(u'1.1'))

    def test_strify(self):
        self.assertEqual('1', strify('1'))
        self.assertEqual('1', strify(1))
        self.assertTupleEqual(('1', '2', '3'), strify((1, 2, 3)))
        self.assertListEqual(['1', '2', '3'], strify([1, 2, 3]))

    def test_random_id(self):
        self.assertNotEqual(random_id(), random_id())
        self.assertEqual(len(random_id(1)), 2)
        self.assertEqual(len(random_id(22)), 44)
        self.assertEqual(len(random_id(256)), 512)
        self.assertEqual(len(random_id(32768)), 65536)
