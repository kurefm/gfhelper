# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-21 21:05
# author:  kurefm

from __future__ import division
from unittest import TestCase
from gfhelper import cv
from PIL import Image


class TestCv(TestCase):
    def test_color(self):
        color = cv.Color('#ffffff')
        self.assertTupleEqual(color.rgb(), (255, 255, 255))
        self.assertEqual(color.hex(), '#FFFFFF')
        self.assertEqual(color, cv.Color(255, 255, 255))
        colors = ['#fffff1', (0x20, 20, 1), (9, 9, 9)]
        colors = map(cv.Color, colors)
        self.assertNotIn(color, colors)
        colors.append(cv.Color(255, 255, 255))

    def test_check(self):
        img = Image.open('tests/resources/test_img1.png')
        params = cv.CvDetectionParams(
            'd4aaccaeecae8cad4ca944a94ca968a948894a594e9444f464d5649624e62462',
            'dhash',
            [37, 40, 280, 100],
            ['#ffffff']
        )

        self.assertTrue(cv.check(img, params))

    def test_read_hp(self):
        img = Image.open('tests/resources/test_img1.png').convert('RGB')
        img = img.crop((1188, 897, 1345, 928))
        cv.filter_color(img, (
            '#5aae5a',
            '#63b263',
            '#63ae5a',
            '#63b25a'
        ))

        pixels = img.load()

        total = img.size[0]

        hp = 0
        for i in range(total):
            if pixels[i, 0] != (0, 0, 0):
                hp += 1

        print hp * 100 / total < 30
