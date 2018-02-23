#!/usr/bin/env python
# coding: utf-8

from gfhelper.app import app

app.setup()

import core
import b02
import logging
import time
import notify2

if __name__ == '__main__':
    notify2.init('gfhelper')

    logging.getLogger().debug("---------- START ----------")

    start_at = time.time()

    core.random_wait()

    b02.auto_battle()
    core.std_wait()
    b02.change_bully()
    core.std_wait()

    notify2.Notification('GfHelper', 'Round 1 finish.').show()

    b02.auto_battle()
    core.std_wait()
    b02.change_bully()

    notify2.Notification(
        'GfHelper',
        'Script run end.\nScript run end.\nScript run end.\nScript run end.\nScript run end.'
    ).show()

    logging.getLogger("Main").info("Run time %ds" % (time.time() - start_at))

    logging.getLogger().debug("---------- END ----------")
