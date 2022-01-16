from math import sin, cos, acos

from main_functions import *
from persons_and_camera import Weapon
import csv
from enums import Enum


class PlayerStates(Enum):
    Normal = 0,
    Dead = 1


class AttributeValue:
    def __init__(self, max_value=0.0, current_value=0.0):
        self.current_value = current_value
        self.max_value = max_value

    def __repr__(self):
        return int(self.current_value)


class PlayerAttributes:
    @staticmethod
    def init():
        attributes = {}
        csv_file = open("hero_stats.csv", encoding="utf8", newline="")
        reader = list(csv.DictReader(csv_file, fieldnames=["name", "value"], delimiter=";"))[1:]

        for row in reader:
            attributes[Attributes.from_name(row["name"])] = AttributeValue(float(row["value"]),
                                                                           float(row["value"]))

        return attributes


class Hero(pygame.sprite.Sprite, PlayerAttributes):
    def __init__(self, village, village_size, inventory):
        super().__init__(village.player_sprites, village.all_sprites)

        pos = random.choice([(village_size // 4, village_size // 2),
                             (village_size // 4 * 3, village_size // 2),
                             (village_size // 2, village_size // 4),
                             (village_size // 2, village_size // 4 * 3)])
        # Переменные, основные
        self.image = pygame.transform.scale(load_image('hero.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * CELL_SIZE
        self.rect.y = int(pos[1]) * CELL_SIZE
        # Переменные, атака
        self.is_attack = [False, False]
        self.angle_attack_range = None
        self.angle_attack_move = None
        self.count_attack = -1
        # Переменные, прочие
        self.state = PlayerStates.Normal
        self.directions = {(0, -STEP): False, (-STEP, 0): False, (0, STEP): False, (STEP, 0): False}
        self.attributes = PlayerAttributes.init()
        self.inventory = inventory

    def damage(self, dmg):
        if self.state == PlayerStates.Normal:
            self.attributes[Attributes.Health].current_value -= dmg
            if self.attributes[Attributes.Health].current_value < 1:
                self.state = PlayerStates.Dead
                self.attributes[Attributes.Health].current_value = AttributeValue()
        return self.state

    def move_player(self, direction, other):
        # Проверка нужно ли идти в данную сторону
        if direction[1]:
            # Движение в эту сторону
            x = direction[0][0] * self.attributes[Attributes.Move_Speed].current_value
            y = direction[0][1] * self.attributes[Attributes.Move_Speed].current_value
            self.rect = self.rect.move(x, y)
            # Если герой врезался во что то, то возвращаем назад
            collide = False
            if pygame.sprite.spritecollideany(self, other.trees_sprites):
                collide = True
            for sprite in other.houses_sprites:
                if pygame.sprite.collide_mask(self, sprite):
                    collide = True
                    break
            for sprite in other.townhall_sprites:
                if pygame.sprite.collide_mask(self, sprite):
                    collide = True
                    break
            if collide:
                self.rect = self.rect.move(-x, -y)

    @staticmethod
    def search_angle():
        # Переменные
        mouse = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        # Формула
        change = mouse - PLAYER_CENTER
        angle = -round(90 - acos(cos(change.y / ((change.x ** 2 + change.y ** 2) ** 2 * 10 ** 3))) * 100)
        # Выравнивание градуса угла
        if mouse.y >= PLAYER_CENTER.y:
            if mouse.x >= PLAYER_CENTER.x:
                angle = 10 - angle
                angle_move = MIN_COE * abs(angle // STEP_ANGLE)
            else:
                angle = angle - 10
                angle_move = MAX_COE - (MIN_COE * abs(angle // STEP_ANGLE))
        else:
            if mouse.x >= PLAYER_CENTER.x:
                angle -= 190
                angle_move = MAX_COE - (MIN_COE * abs(angle // STEP_ANGLE))
            else:
                angle = 190 - angle
                angle_move = MIN_COE * abs(angle // STEP_ANGLE)

        return [angle, angle_move]

    def step_and_draw_attack(self, size_step_attack):
        radius = 45
        # Отрисовка
        self.weapon.image = pygame.transform.rotate(self.weapon.image, self.angle_attack_range)
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.x = PLAYER_CENTER.x + radius * sin(self.angle_attack_move)
        self.weapon.rect.y = PLAYER_CENTER.y + radius * cos(self.angle_attack_move)
        # Шаг
        self.angle_attack_range -= STEP_ANGLE * size_step_attack
        self.angle_attack_move -= MIN_COE * size_step_attack
        self.count_attack -= 1

    def attack(self, village):
        # Очистка
        for sword in village.sword_sprites:
            village.sword_sprites.remove(sword)
        self.weapon = Weapon(village)
        # Обычная атака
        if self.is_attack[0]:
            size_step_attack = 8
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = self.search_angle()[0] + 40, self.search_angle()[
                    1] + MIN_COE * 40
                self.count_attack = 10
            # Отрисовка и шаг
            self.step_and_draw_attack(size_step_attack)
            # Атака
            self.weapon.attack(self.attributes[Attributes.Damage].current_value, village)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack[0] = False
        # Круговая атака
        elif self.is_attack[1]:
            size_step_attack = 12
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = self.search_angle()
                self.count_attack = 360 // size_step_attack
            # Отрисовка и шаг
            self.step_and_draw_attack(size_step_attack)
            # Атака
            self.weapon.attack(self.attributes[Attributes.Damage].current_value // 2, village)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack[1] = False
        else:
            # Если герой не атакует, то меч удалить
            self.weapon.kill()

    def set_dir(self, event, value):
        if event.key == pygame.K_w:
            self.directions[(0, -STEP)] = value
        if event.key == pygame.K_a:
            self.directions[(-STEP, 0)] = value
        if event.key == pygame.K_s:
            self.directions[(0, STEP)] = value
        if event.key == pygame.K_d:
            self.directions[(STEP, 0)] = value

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if not any(self.is_attack):
                    self.is_attack[0] = True
            if event.button == 3:
                if not any(self.is_attack):
                    self.is_attack[1] = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.attributes[Attributes.Move_Speed].current_value = \
                    self.attributes[Attributes.Move_Speed].max_value * 1.8
            self.set_dir(event, True)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.attributes[Attributes.Move_Speed].current_value = \
                    self.attributes[Attributes.Move_Speed].max_value
            self.set_dir(event, False)
