# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-28 11:53
# author:  kurefm

from unittest import TestCase
from gfhelper import core


@core.script()
def test():
    """
    A test script
    """


class TestCore(TestCase):
    def test_script_decorator(self):
        self.assertIsInstance(test, core.Script)
        self.assertEqual(test.doc(), 'A test script')
