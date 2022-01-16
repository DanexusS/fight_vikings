import random
import pygame
from enums import Enum
from pygame import Vector2


"""Общие"""


WIDTH = 1920
HEIGHT = 1080
BG = '#43485E'
BG_BTN = '#C8D1F7'
BG_BTN_SHADOW = '#242429'
SIZE_MENU_BTN = Vector2(300, 80)


"""Игрок"""


PLAYER_SIZE = 40
STEP = 4
PLAYER_CENTER = Vector2(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2)


"""Для вычисления координат"""


STEP_ANGLE = 1
MIN_COE = 0.017
MAX_COE = (MIN_COE * (360 // STEP_ANGLE))


"""Генерация"""


MAP_SIZE = random.randrange(20, 30, 2)
EMPTY_N = MAP_SIZE // 2
CELL_SIZE = 180
MIN_ROAD = MAP_SIZE // 10
MAX_ROAD = MIN_ROAD * 2
MASK = MAP_SIZE // 5
RANGE_SQUARE = MAP_SIZE // 2.5


"""Инвентарь"""


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Attack_Radius = 2
    Damage = 3
    Health = 4
    Armor = 5
    Stamina = 6


BG_COLOR = pygame.Color("#43485E")
SLOT_COLORS = {
    "Frame": pygame.Color("#C8D1F7"),
    "Hovered_BG": pygame.Color("#60667e"),
    "Info_BG": pygame.Color("#787d91"),
    "Amount_Text": pygame.Color("#d0d1d6"),
}
INV_SLOT_SIZE = 128
RUS_ATTRIBUTES = {
    Attributes.Move_Speed: "скорость",
    Attributes.Attack_Speed: "скорость атаки",
    Attributes.Damage: "урон"
}
