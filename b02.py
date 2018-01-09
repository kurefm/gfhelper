# coding: utf-8

import common
import core
import logging

DEPLOY_POINT_1 = 922, 478, 1048, 604  # 指挥部
DEPLOY_POINT_2 = 346, 481, 436, 571  # 机场LB

ATTACK_POINT_1_BEFORE = 698, 346, 799, 447
ATTACK_POINT_1_AFTER = 698, 489, 799, 590
ATTACK_POINT_2_BEFORE = 756, 174, 847, 265
ATTACK_POINT_2_AFTER = 756, 494, 847, 585
PASSING_POINT_2_3 = 954, 181, 1055, 282
ATTACK_POINT_3 = 734, 342, 834, 442
ATTACK_POINT_4 = 1164, 337, 1264, 437
ATTACK_POINT_5 = 1426, 380, 1551, 505

ECHELON_COUNT = 3
MAIN_ECHELON = 1
SUPPLY_ECHELON = 2

G11_REGION = 0
FAL_REGION = 0

__logger = logging.getLogger(__name__)


def enter_battle():
    common.combat()
    core.std_wait()
    common.select_battle('0-2')
    core.random_wait()
    common.normal_battle()


def deploy_echelon():
    common.press(DEPLOY_POINT_1)
    core.random_wait()
    # common.select_echelon(MAIN_ECHELON, ECHELON_COUNT) #顺序部署，可以简化
    # core.random_wait()
    common.ack_deploy()
    __logger.info("Deploy main echelon")

    core.random_wait()

    common.press(DEPLOY_POINT_2)
    core.random_wait()
    # common.select_echelon(SUPPLY_ECHELON - 1, ECHELON_COUNT - 1) #顺序部署，可以简化
    # core.random_wait()
    common.ack_deploy()
    __logger.info("Deploy supply echelon")


def supply():
    common.press(DEPLOY_POINT_2)
    core.random_wait_lite()
    common.press(DEPLOY_POINT_2)
    core.random_wait()
    common.supply()


def attack_1():
    common.press(DEPLOY_POINT_1)
    core.random_wait_lite()
    common.press(ATTACK_POINT_1_BEFORE)
    __logger.info("Attack point 1")
    core.std_wait()
    core.wait_fight_end()
    common.finish_fight()


def attack_2():
    common.press(ATTACK_POINT_1_AFTER)
    core.random_wait_lite()
    common.press(ATTACK_POINT_2_BEFORE)
    __logger.info("Attack point 2")
    core.std_wait()
    core.wait_fight_end()
    common.finish_fight()


def attack_3():
    common.press(ATTACK_POINT_2_AFTER)
    core.random_wait_lite()
    common.press(PASSING_POINT_2_3)
    core.std_wait()
    core.scroll_up(400)
    core.random_wait_lite()
    common.press(ATTACK_POINT_3)
    __logger.info("Attack point 3")
    core.std_wait()
    core.wait_fight_end(20000)
    common.finish_fight()


def attack_4():
    common.press(ATTACK_POINT_3)
    core.random_wait_lite()
    common.press(ATTACK_POINT_4)
    __logger.info("Attack point 4")
    core.std_wait()
    core.wait_fight_end(22000)
    common.finish_fight()


def attack_5():
    common.press(ATTACK_POINT_4)
    core.random_wait_lite()
    common.press(ATTACK_POINT_5)
    __logger.info("Attack point 5")
    core.std_wait()
    core.wait_fight_end(22000)
    common.finish_fight()


def use_g11():
    common.formation()
    core.std_wait()

    # common.formation_echelon(1)
    # core.random_wait()

    common.change_people(4)
    core.random_wait_lite(2)
    common.select_people(1, 4)
    core.random_wait()

    common.formation_echelon(2)
    common.formation_echelon(2)
    core.random_wait()

    common.change_people(1)
    core.random_wait_lite(2)
    common.select_people(2, 2)
    core.random_wait_lite(2)
    common.back()


def use_fal():
    common.formation()
    core.std_wait()

    # common.formation_echelon(1)
    # core.random_wait()

    common.change_people(4)
    core.random_wait_lite(2)
    common.select_people(2, 2)
    core.random_wait()

    common.formation_echelon(2)
    common.formation_echelon(2)
    core.random_wait()

    common.change_people(1)
    core.random_wait_lite(2)
    common.select_people(1, 4)
    core.random_wait_lite(2)
    common.back()


def auto_battle():
    enter_battle()
    core.std_wait()

    deploy_echelon()
    core.random_wait()

    common.start_battle()
    core.std_wait()

    supply()
    core.std_wait()

    attack_1()
    core.std_wait()

    attack_2()
    core.std_wait()

    attack_3()
    core.std_wait()

    common.end_round()
    core.std_wait()
    core.wait(12000)
    core.random_wait()

    attack_4()
    core.std_wait()

    attack_5()
    core.std_wait()

    common.end_battle()
