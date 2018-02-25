# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 16:50
# author:  kurefm

"""
用于0-2拖尸
"""

from gfhelper.app import app
from gfhelper.cli import command

from gfhelper import core, formation, combat, cv

import imagehash
import click
import logging

c = app.config.get

logger = logging.getLogger(__name__)


def use_killer1():
    formation.select_echelon(c('b02.main_echelon'))
    formation.change_doll(c('b02.killer_pos'))
    formation.select_doll(*c('b02.killer1.pos'))
    formation.select_echelon(c('b02.supply_echelon'))
    formation.change_doll(1)
    formation.select_doll(*c('b02.killer2.pos'))


def use_killer2():
    formation.select_echelon(c('b02.main_echelon'))
    formation.change_doll(c('b02.killer_pos'))
    formation.select_doll(*c('b02.killer2.pos'))
    formation.select_echelon(c('b02.supply_echelon'))
    formation.change_doll(1)
    formation.select_doll(*c('b02.killer1.pos'))


def killer_hash():
    box = app.config.get('formation.change_people.box_model')
    region = box[c('b02.killer_pos') - 1]
    return imagehash.dhash(core.screencap().crop(region), 16)


@command()
@click.argument('name', type=str)
def update_killer(name):
    """
    更新打手的识别hash
    """
    app.config.set('b02.%s.dhash' % name, str(killer_hash()))
    app.config.save()


@command()
def switch_killer():
    """
    交换打手
    """
    with formation.formation():
        formation.select_echelon(c('b02.main_echelon'))
        if cv.cmp_hash(killer_hash(), c('b02.killer1.dhash')): use_killer2()
        if cv.cmp_hash(killer_hash(), c('b02.killer2.dhash')): use_killer1()


@command()
def auto_battle():
    """
    自动进行一轮战斗
    """
    combat.enter()
    combat.select_battle('0-2')
    combat.normal_battle()
    combat.fairy_skill_auto_off()
    logger.info('Deploy echelon')
    combat.deploy_on(c('b02.killer_deploy'))
    combat.deploy_on(c('b02.supply_deploy'))
    combat.start_battle()

    # supply
    core.tap(c('b02.supply_deploy'))
    core.tap(c('b02.supply_deploy'))
    combat.supply()

    # attack_point1
    logger.info('Attack 1')
    core.tap(c('b02.killer_deploy'))
    combat.attack(c('b02.attack1'))
    core.wait(c('b02.attack_duration'))
    combat.quick_end_fight()

    # attack_point2
    logger.info('Attack 2')
    core.tap(c('b02.attack1e'))
    combat.attack(c('b02.attack2'))
    core.wait(c('b02.attack_duration'))
    combat.quick_end_fight()


    # attack_point3
    logger.info('Attack 3')
    core.tap(c('b02.attack2e'))
    core.tap(c('b02.passing'))
    combat.wait_walk()
    core.scroll_up(400)
    combat.attack(c('b02.attack3'))
    core.wait(c('b02.attack_duration'))
    combat.quick_end_fight()
    combat.end_round()
    combat.ensure_in_battle()
    core.wait(2000)

    # attack_point4
    logger.info('Attack 4')
    core.tap(c('b02.attack3'))
    combat.attack(c('b02.attack4'))
    core.wait(c('b02.attack_duration'))
    combat.end_fight()

    # attack_point5
    logger.info('Attack 5')
    core.tap(c('b02.attack4'))
    combat.attack(c('b02.attack5'))
    core.wait(c('b02.attack_duration'))
    combat.quick_end_fight()
    combat.quick_end_battle()


@command()
def run():
    ctx = click.get_current_context()
    ctx.forward(auto_battle)
