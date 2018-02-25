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

__traceable = tracer.traceable
__inject_args = app.config.inject_args
__logger = logging.getLogger(__name__)


def parse_battle_name(name):
    return re.match(r'^(\d{0,2})-(\d)([en]*?)$', name).groups()


@__traceable('combat')
@__inject_args()
def enter(config):
    tap(config['region'])
    cv.ensure(screencap, config['cv_detection'], '未检测到战斗选择界面')


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
def select_battle(name):
    ep, no, d = parse_battle_name(name)
    select_episode(int(ep))
    select_difficulty(d)
    box = app.config.get('combat.select_battle.no.box_model')
    tap(box[int(no) - 1, 0])
    cv.ensure(screencap, app.config.get('combat.select_battle.no.cv_detection'))


@__traceable('combat')
@__inject_args()
def normal_battle(config):
    tap(config['region'])
    __logger.info('Enter normal battle')
    cv.ensure(screencap, config['cv_detection'])
    __logger.info('Current in battle prepare')


@__traceable()
def select_echelon(no, count):
    pass


@__traceable('combat')
@__inject_args('combat.in_select')
def ensure_in_select(cvd):
    cv.ensure(screencap, cvd, '未检测到梯队界面')
    __logger.debug('Current in echelon')


@__traceable('combat')
@__inject_args('combat.in_battle')
def ensure_in_battle(cvd):
    cv.ensure(screencap, cvd, '未检测到战役界面')
    __logger.debug('Current in battle')


@__traceable('combat')
@__inject_args('combat.in_fight')
def ensure_in_fight(cvd):
    cv.ensure(screencap, cvd, '未检测到战斗界面')
    __logger.debug('Current in fight')


@__traceable('combat')
@__inject_args('combat.in_settlement')
def ensure_in_settlement(cvd):
    cv.ensure(screencap, cvd, '未检测到战斗结算界面')


@__traceable('combat')
@__inject_args(
    'combat.ack_deploy',
    'combat.normal_battle.cv_detection'
)
def ack_deploy(region, cvd):
    tap(region)
    cv.ensure(screencap, cvd)


@__traceable()
def deploy_on(region):
    tap(region)
    ensure_in_select()
    ack_deploy()


@__traceable('combat')
@__inject_args()
def start_battle(region):
    tap(region)
    ensure_in_battle()
    wait(1500)


@__traceable('combat')
@__inject_args()
def supply(region):
    ensure_in_select()
    tap(region)
    ensure_in_battle()
    __logger.info('Supplied')


@__traceable()
def wait_walk():
    wait(app.config.get('combat.walk_duration'))


@__traceable()
def attack(region):
    tap(region)
    wait_walk()
    ensure_in_fight()


@__traceable('combat')
@__inject_args('combat.get_doll')
def end_fight(cvd):
    __logger.info('Wait fight end')
    ensure_in_settlement()
    tap_center()
    tap_center()
    wait(500)
    if cv.check(screencap(), cvd):
        __logger.info('Got doll/equip')
        tap_center()
        tap_center()
    ensure_in_battle()


@__traceable()
def quick_end_fight(got_doll=True):
    __logger.info('Wait fight end')
    ensure_in_settlement()
    tap_center()
    tap_center()
    if got_doll:
        tap_center()
        tap_center()
    ensure_in_battle()


@__traceable('combat')
@__inject_args()
def end_round(region):
    ensure_in_battle()
    tap(region)
    wait(1000)
    __logger.info('End current round')


@__traceable('combat')
@__inject_args(
    'combat.end_round',
    'combat.battle_settlement',
    'combat.get_doll',
    'formation.back.cv_detection'
)
def end_battle(region, cvd1, cvd2, cvd3):
    ensure_in_battle()
    tap(region)
    __logger.info('Wait battle end')
    cv.ensure(screencap, cvd1, '未检测到战役结算界面')
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
    cv.ensure(screencap, cvd3, '未检测到主界面')


@__traceable()
def quick_end_battle(got_doll=True):
    ensure_in_battle()
    tap(app.config.get('combat.end_round'))
    __logger.info('Wait battle end')
    cv.ensure(screencap, app.config.get('combat.battle_settlement'), '未检测到战役结算界面')
    tap_center()
    tap_center()
    tap_center()
    if got_doll:
        tap_center()
        tap_center()
    cv.ensure(screencap, app.config.get('formation.back.cv_detection'), '未检测到主界面')


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
