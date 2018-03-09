# coding: utf-8
# 
# project: gfhelper
# date:    2018-01-22 12:24
# author:  kurefm

from .app import app
from .tracer import tracer
from .core import screencap, wait, tap, tap_center
from . import cv
import logging
import re
import contextlib

__traceable = tracer.traceable
__inject_args = app.config.inject_args
__logger = logging.getLogger(__name__)

c = app.config.get


def parse_battle_name(name):
    return re.match(r'^(\d{0,2})-(\d)([en]*?)$', name).groups()


@__traceable('combat')
@__inject_args()
def enter(config):
    tap(config['region'])
    wait(2000)
    cv.ensure(screencap, config['cv_detection'], '未检测到战斗选择界面')


@__traceable('combat')
@__inject_args()
def back(region):
    tap(region)
    wait(500)


@__traceable()
def select_episode(ep):
    box = app.config.get('combat.select_battle.episode.box_model')
    region = box[ep, 0]
    colors = app.config.get('combat.select_battle.episode.selected_color')
    while not cv.has_color(screencap().crop(region), colors):
        tap(region)
        wait(500)
    __logger.info('Select Ep.%s' % ep)


@__traceable()
def select_difficulty(d):
    box = app.config.get('combat.select_battle.difficulty.box_model')
    index = 0
    if d == 'e': index = 1
    if d == 'n': index = 2

    sample_region = app.config.get('combat.select_battle.difficulty.color_sample')
    colors = app.config.get('combat.select_battle.difficulty.selected_color')[index]

    if not cv.has_color(screencap().crop(sample_region), colors):
        tap(box[index])
    wait(500)
    cv.ensure_color(lambda: screencap().crop(sample_region), colors)


@__traceable()
def select_battle(name, quick=False):
    ep, no, d = parse_battle_name(name)
    if not quick:
        select_episode(int(ep))
        select_difficulty(d)
    box = app.config.get('combat.select_battle.no.box_model')
    tap(box[int(no) - 1, 0])
    cv.ensure(screencap, app.config.get('combat.select_battle.no.cv_detection'))


@__inject_args()
def normal_battle(config):
    tap(config['region'])
    __logger.info('Enter normal battle')
    wait(500)
    if cv.check(screencap(), c('combat.is_max')):
        tap(c('combat.is_max')[0].crop)
        tap(c('combat.exit_battle_setting'))
        wait(200)
        return False
    cv.ensure(screencap, config['cv_detection'], '等待进入战役准备界面')
    __logger.info('Current in battle prepare')
    return True


@__traceable()
def select_echelon(no, count):
    pass


@__traceable('combat')
@__inject_args('combat.in_select')
def wait_into_select(cvd):
    cv.ensure(screencap, cvd, '等待进入梯队界面')
    __logger.debug('Current in echelon')


@__traceable('combat')
@__inject_args('combat.in_battle')
def wait_into_battle(cvd):
    cv.ensure(screencap, cvd, '等待进入战役界面')
    __logger.debug('Current in battle')


@__traceable('combat')
@__inject_args('combat.in_fight')
def wait_into_fight(cvd):
    cv.ensure(screencap, cvd, '等待进入战斗界面')
    __logger.debug('Current in fight')


@__traceable('combat')
@__inject_args('combat.in_settlement')
def wait_into_fight_settlement(cvd):
    cv.ensure(screencap, cvd, '等待进入战斗结算界面')


@__traceable('combat')
@__inject_args(
    'combat.ack_deploy',
    'combat.normal_battle.cv_detection'
)
def ack_deploy(region, cvd):
    tap(region)
    wait(500)
    cv.ensure(screencap, cvd)


@__traceable()
def deploy_on(region):
    tap(region)
    wait(500)
    wait_into_select()
    ack_deploy()


@__traceable()
def start_battle():
    tap(c('combat.start_battle.region'))
    wait(500)
    wait_into_battle()
    wait(500)
    if cv.check(screencap(), c('combat.start_battle.is_midnight')):
        tap(c('combat.start_battle.close_tips'))
        wait(500)


@__traceable('combat')
@__inject_args()
def supply(region):
    wait_into_select()
    tap(region)
    wait(500)
    wait_into_battle()
    __logger.info('Supplied')


@__traceable()
def wait_walk():
    wait(app.config.get('combat.walk_duration'))


@__traceable()
def attack(region):
    tap(region)
    wait_walk()
    wait_into_fight()


@__traceable('combat')
@__inject_args('combat.get_doll')
def end_fight(cvd):
    __logger.info('Wait fight end')
    wait_into_fight_settlement()
    wait(500)
    tap_center()
    tap_center()
    wait(500)
    if cv.check(screencap(), cvd):
        __logger.info('Got doll/equip')
        tap_center()
        tap_center()
    wait_into_battle()


@__traceable()
def quick_end_fight(got_doll=True):
    __logger.info('Wait fight end')
    wait_into_fight_settlement()
    tap_center()
    tap_center()
    if got_doll:
        tap_center()
        tap_center()
    wait(500)
    times = 0
    while not cv.check(screencap(), app.config.get('combat.in_battle')):
        if times > 3: tap_center()
        __logger.info('等待进入战役界面')
        times += 1
        wait(500)
    __logger.info('Current in battle')


@__traceable('combat')
@__inject_args()
def end_round(region):
    wait_into_battle()
    tap(region)
    __logger.info('End current round')


@__traceable('combat')
@__inject_args(
    'combat.end_round',
    'combat.battle_settlement',
    'combat.get_doll',
    'formation.back.cv_detection'
)
def end_battle(region, cvd1, cvd2, cvd3):
    wait_into_battle()
    tap(region)
    __logger.info('Wait battle end')
    wait(3000)
    cv.ensure(screencap, cvd1, '等待进入战役结算界面')
    tap_center()
    tap_center()
    wait(500)
    if cv.check(screencap(), cvd2):
        __logger.info('Got doll/equip')
        tap_center()
        tap_center()
    else:
        tap_center()
        wait(500)
        if cv.check(screencap(), cvd2):
            __logger.info('Got doll/equip')
            tap_center()
            tap_center()


@__traceable()
def quick_end_battle(got_doll=True):
    tap(app.config.get('combat.end_round'))
    __logger.info('Wait battle end')
    wait(3000)
    cv.ensure(screencap, app.config.get('combat.battle_settlement'), '等待进入战役结算界面')
    tap_center()
    tap_center()
    tap_center()
    if got_doll:
        tap_center()
        tap_center()


@__traceable('combat')
@__inject_args(
    'combat.fairy_skill.use.region'
)
def use_fairy_kill(region):
    tap(region)
    wait(500)


@__traceable('combat')
@__inject_args(
    'combat.fairy_skill.auto.region',
    'combat.fairy_skill.auto.color_sample',
    'combat.fairy_skill.auto.on_color'
)
def fairy_skill_auto_on(region, sample, colors):
    if not cv.has_color(screencap().crop(sample), colors):
        tap(region)
        cv.ensure_color(lambda: screencap().crop(sample), colors)


@__traceable('combat')
@__inject_args(
    'combat.fairy_skill.auto.region',
    'combat.fairy_skill.auto.color_sample',
    'combat.fairy_skill.auto.on_color'
)
def fairy_skill_auto_off(region, sample, colors):
    if cv.has_color(screencap().crop(region), colors):
        tap(region)
        cv.ensure_not_color(lambda: screencap().crop(sample), colors)


@__traceable()
def toggle_auto_skill():
    pass


@__traceable()
def withdraw():
    tap(c('combat.withdraw.region'))
    wait(500)
    if cv.check(screencap(), c('combat.withdraw.dialog.cv_detection')):
        tap(c('combat.withdraw.dialog.ack'))
    wait(1000)


def exit_battle():
    tap(c('combat.exit_battle'))
    wait(500)
    cv.ensure(screencap, c('combat.enter.cv_detection'), '等待进入战斗选择界面')


def stop_battle():
    tap(c('combat.stop_battle.region'))
    wait(500)
    tap(c('combat.stop_battle.dialog.ack'))
    wait(500)


@__traceable('combat')
@__inject_args()
def enter_formation(config):
    tap(config['region'])
    wait(500)
    cv.ensure(screencap, config['cv_detection'], '等待进入队伍编成界面')


@__traceable()
def exit_formation():
    tap(c('formation.back'))
    wait(500)


@__traceable()
def select_doll(row, col):
    box = app.config.get('formation.select_people.box_model')
    tap(box[row - 1, col - 1])
    wait(500)
    while cv.check(screencap(), app.config.get('formation.change_people.cv_detection')):
        tap(box[row - 1, col - 1])
        wait(500)
    cv.ensure(screencap, app.config.get('combat.enter_formation.cv_detection'), '等待进入队伍编成界面')


@contextlib.contextmanager
def formation():
    enter_formation()
    yield
    exit_formation()
    wait_into_battle()
