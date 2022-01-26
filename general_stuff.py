"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import random
import pygame
import math

from pygame import Vector2
import item_database
from item_database import Attributes


def load_image(name):
    return pygame.image.load(f"images/{name}").convert_alpha()


def size_img(name, num=1):
    return pygame.transform.scale(load_image(name), (GAME_CELL_SIZE * num, GAME_CELL_SIZE * num))


def step_and_draw_attack(creature, size_step_attack, center):
    radius = 45
    # Отрисовка
    creature.weapon.image = pygame.transform.rotate(creature.weapon.image, creature.angle_attack_range)
    creature.weapon.rect = creature.weapon.image.get_rect()
    creature.weapon.rect.x = center.x + radius * math.sin(creature.angle_attack_move)
    creature.weapon.rect.y = center.y + radius * math.cos(creature.angle_attack_move)
    # Шаг
    creature.angle_attack_range -= STEP_ANGLE * size_step_attack
    creature.angle_attack_move -= MIN_COE * size_step_attack
    creature.count_attack -= 1


def search_angle(xy1, xy2):
    # Формула
    change = xy1 - xy2
    # Формула
    sqrt1 = math.sqrt((change.x + 1) * (change.x + 1) + (change.y + 1) * (change.y + 1))
    angle = -round(90 - math.acos(math.cos((change.y * 10) / ((sqrt1 * 10) + 1))) * 100)
    # Выравнивание градуса угла
    if xy1.y >= xy2.y:
        if xy1.x >= xy2.x:
            angle = 10 - angle
            angle_move = MIN_COE * abs(angle // STEP_ANGLE)
        else:
            angle = angle - 10
            angle_move = MAX_COE - (MIN_COE * abs(angle // STEP_ANGLE))
    else:
        if xy1.x >= xy2.x:
            angle -= 190
            angle_move = MAX_COE - (MIN_COE * abs(angle // STEP_ANGLE))
        else:
            angle = 190 - angle
            angle_move = MIN_COE * abs(angle // STEP_ANGLE)

    return [angle, angle_move]


class GameMouseData:
    def __init__(self):
        self.current_interface = None
        self.start_drag_slot = None
        self.slot_hovered_over = None
        self.position = Vector2()


"""Общие"""


WIDTH = 1920
HEIGHT = 1080
BG = '#43485E'
BG_BTN = '#C8D1F7'
BG_BTN_SHADOW = '#242429'
SIZE_MENU_BTN = Vector2(300, 80)
MOUSE = GameMouseData()
ITEMS_DB = item_database.init()


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
GAME_CELL_SIZE = 180
MIN_ROAD = MAP_SIZE // 10
MAX_ROAD = MIN_ROAD * 2
MASK = MAP_SIZE // 5
RANGE_SQUARE = MAP_SIZE // 2.5


"""Инвентарь"""


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
    Attributes.Attack_Radius: "радиус атаки",
    Attributes.Damage: "урон",
    Attributes.Health: "здоровье",
    Attributes.Armor: "броня",
    Attributes.Stamina: "выносливость"
}
