#!/usr/bin/env python
# coding: utf-8


import common
import core
import b02
import logging
import time
from logging.config import fileConfig

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s | %(name)-6s | %(levelname)-5s : %(message)s",
    )

    logging.getLogger().debug("---------- START ----------")

    start_at = time.time()

    core.random_wait()

    b02.auto_battle()
    core.std_wait()
    b02.use_fal()
    core.std_wait()

    b02.auto_battle()
    core.std_wait()
    b02.use_g11()

    logging.getLogger("Main").info("Run time %ds" % (time.time() - start_at))

    logging.getLogger().debug("---------- END ----------")
