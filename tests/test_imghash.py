# coding: utf-8
# 
# project: gfhelper
# date:    2018-02-02 17:39
# author:  kurefm

import imagehash
from PIL import Image
from unittest import TestCase
import cStringIO
import cv2
import numpy as np


class TestImageHash(TestCase):
    def test_phash(self):
        cz75 = imagehash.phash(Image.open('/home/kurefm/Downloads/cz75.png'), 36, 18)
        iws2000 = imagehash.phash(Image.open('/home/kurefm/Downloads/iws2000.png'), 36, 18)

        get_cz75 = imagehash.phash(Image.open('screenshot/get-cz75.png'), 36, 18)
        get_iws2000 = imagehash.phash(Image.open('screenshot/get-iws2000.png'), 36, 18)

    def test_image(self):
        Image
        img = Image.open('screenshot/g11-on-echelon1.png')
        img = img.crop((1056, 310, 1296, 550))
        print imagehash.dhash(img, 16)
