import os
import math
from constants import *


def load_image(name):
    fullname = os.path.join('images/', name)
    return pygame.image.load(fullname).convert_alpha()


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
