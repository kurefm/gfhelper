# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-21 21:05
# author:  kurefm

from __future__ import division
from unittest import TestCase
from gfhelper import cv, factory
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

    def test_read_rarity(self):
        img = Image.open('/home/kurefm/.config/gfhelper/screenshot/factory-select-doll.png').convert('RGB')

        # cv.filter_color(img, ('#ffbe00', '#ffba00'))

        # print factory.read_rarity(img.crop(factory.doll_region(1, 2)))

        for row in [1, 2]:
            for col in [1, 2, 3, 4, 5, 6]:
                print factory.read_rarity(img.crop(factory.doll_region(row, col)))

    def test_map_hash(self):
        img = Image.open('/home/kurefm/.config/gfhelper/screenshot/0-2.png').convert('RGB')
        cv.filter_color(img, (
            '#ff0000',
            '#94c2f7',
            '#94c6ff',
            '#94c6f7',
            '#9ccaff',
        ))
        img.show()
