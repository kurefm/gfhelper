# coding: utf-8

from random import randrange
import core
import logging
from PIL import Image
import imagehash
from cStringIO import StringIO
from gfhelper.core import screencap

RESERVED_OFFSET = 10

# 矩形区域 (LT-x, LT-y, RB-x, RB-y)
# 圆形区域 (x, y, R)

COMBAT_REGION = 1238, 651, 1532, 843
FORMATION_REGION = 1585, 627, 1878, 819

BATTLE_A_REGION = (
    (287, 154, 478, 285),  # 0-B
)

BATTLE_B_REGION = (
    (631, 349, 1897, 487),  # A-1
    (631, 526, 1897, 664),  # A-2
)

NORMAL_BATTLE_REGION = 1005, 816, 1233, 922
AUTONOMIC_BATTLE_REGION = 0, 0, 0, 0
START_BATTLE_REGION = 1500, 907, 1901, 1059

ECHELON_HEIGHT = 109
ECHELON_WIDTH = 182
DEPLOY_ECHELON_PADDING = 37
FORMATION_ECHELON_PADDING = 20

FORMATION_ECHELON_MARGIN_TOP = 161
CHANGE_PEOPLE_MARGIN_LEFT = 215
CHANGE_PEOPLE_MARGIN_TOP = 234
PEOPLE_WIDTH = 262
PEOPLE_HEIGHT = 455
PEOPLE_MARGIN = 14

SELECT_PEOPLE_MARGIN_TOP = 166
SELECT_PEOPLE_MARGIN_LEFT = 10
SELECT_PEOPLE_PADDING_BOTTOM = 24
SELECT_PEOPLE_PADDING_RIGHT = 24
SELECT_PEOPLE_WIDTH = 244
SELECT_PEOPLE_HEIGHT = 432

ACK_DEPLOY_REGION = 1646, 925, 1893, 1019
CANCEL_DEPLOY_REGION = 0, 0, 0, 0

SUPPLY_REGION = 1622, 794, 1918, 887

END_ROUND_REGION = 1648, 932, 1883, 1049

BACK_REGION = 6, 6, 198, 137

TOGGLE_PLAN_MODE = 0, 854, 214, 919
EXEC_PLAN = 1654, 921, 1903, 1030

__logger = logging.getLogger(__name__)


def rect_incircle(region):
    """
    计算矩形区域的内接圆
    :param region:
    :return:
    """
    return (
        (region[0] + region[2]) / 2,
        (region[1] + region[3]) / 2,
        min(region[2] - region[0], region[3] - region[1])
    )


def random_point(region):
    if len(region) == 4:
        return (
            randrange(region[0] + RESERVED_OFFSET, region[2] - RESERVED_OFFSET),
            randrange(region[1] + RESERVED_OFFSET, region[3] - RESERVED_OFFSET)
        )
    elif len(region) == 3:
        pass
    else:
        return 0, 0


def press(region):
    core.press(*random_point(region))


def combat():
    press(COMBAT_REGION)


def formation():
    press(FORMATION_REGION)


def select_battle(name):
    a = int(name[0])
    b = int(name[2]) - 1
    t = name[3] if len(name) == 4 else None

    press(BATTLE_A_REGION[a])
    press(BATTLE_A_REGION[a])
    core.random_wait_lite(2)
    press(BATTLE_B_REGION[b])
    __logger.info("Select battle " + name)


def normal_battle():
    press(NORMAL_BATTLE_REGION)


def select_echelon(no, count):
    # FIXME 超出屏幕高度时需要调整
    margin_top = (1080 - (ECHELON_HEIGHT * (count + 1) + DEPLOY_ECHELON_PADDING * count)) / 2
    top_offset = (ECHELON_HEIGHT + DEPLOY_ECHELON_PADDING) * (no - 1)
    press((
        0,
        margin_top + top_offset,
        ECHELON_WIDTH,
        margin_top + top_offset + ECHELON_HEIGHT
    ))
    __logger.info("Select echelon no {0} from {1}".format(no, count))


def ack_deploy():
    __logger.info("Ack deploy")
    press(ACK_DEPLOY_REGION)


def start_battle():
    __logger.info("Start battle")
    press(START_BATTLE_REGION)


def supply():
    __logger.info("Supply")
    press(SUPPLY_REGION)


def finish_fight():
    __logger.info("Finish fight")
    core.press_center()
    core.press_center()

    core.wait(300)

    img = Image.open(StringIO(screencap()))

    img = img.crop((470, 100, 1020, 750))

    hash = imagehash.dhash(img, 16)

    img.save('screenshot/unknown/{}.png'.format(hash))

    core.press_center()
    core.press_center()

    core.wait(1500)


def end_round():
    __logger.info("End round(battle)")
    press(END_ROUND_REGION)


def end_battle():
    end_round()
    core.wait(5000)
    core.std_wait()
    finish_fight()


def formation_echelon(no):
    top_offset = FORMATION_ECHELON_MARGIN_TOP + (ECHELON_HEIGHT + FORMATION_ECHELON_PADDING) * (no - 1)
    press((
        0,
        top_offset,
        ECHELON_WIDTH,
        top_offset + ECHELON_HEIGHT
    ))
    __logger.info("Formation echelon no.{0}".format(no))


def change_people(no):
    left_offset = CHANGE_PEOPLE_MARGIN_LEFT + (PEOPLE_WIDTH + PEOPLE_MARGIN) * (no - 1)
    press((
        left_offset,
        CHANGE_PEOPLE_MARGIN_TOP,
        left_offset + PEOPLE_WIDTH,
        CHANGE_PEOPLE_MARGIN_TOP + PEOPLE_HEIGHT
    ))
    __logger.info("Change people no.{0}".format(no))


def select_people(row, col):
    top_offset = SELECT_PEOPLE_MARGIN_TOP + (SELECT_PEOPLE_HEIGHT + SELECT_PEOPLE_PADDING_BOTTOM) * (row - 1)
    left_offset = SELECT_PEOPLE_MARGIN_LEFT + (SELECT_PEOPLE_WIDTH + SELECT_PEOPLE_PADDING_RIGHT) * (col - 1)
    press((
        left_offset,
        top_offset,
        left_offset + SELECT_PEOPLE_WIDTH,
        top_offset + SELECT_PEOPLE_HEIGHT
    ))
    __logger.info("Select people [{0}, {1}]".format(row, col))


def remove_people():
    select_people(1, 1)


def back():
    press(BACK_REGION)


def toggle_plan_mode():
    press(TOGGLE_PLAN_MODE)


def exec_plan():
    press(EXEC_PLAN)
