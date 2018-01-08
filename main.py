#!/usr/bin/env python
# coding: utf-8


import common
import core
import b02
import logging
import time

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(name)-6s | %(levelname)-5s : %(message)s")

    start_at = time.time()

    b02.auto_battle()
    core.std_wait()
    b02.use_fal()
    core.std_wait()

    b02.auto_battle()
    core.std_wait()
    b02.use_g11()

    logging.getLogger("Main").info("Run time %ds" % (time.time() - start_at))
