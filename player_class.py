"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""
from items import ItemType
from main_functions import *

from csv import DictReader
from weapon_class import Weapon
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
        reader = list(DictReader(csv_file, fieldnames=["name", "value"], delimiter=";"))[1:]

        for row in reader:
            attributes[Attributes.from_name(row["name"])] = AttributeValue(float(row["value"]),
                                                                           float(row["value"]))

        return attributes


class Hero(pygame.sprite.Sprite):
    def __init__(self, village, village_size, inventory, equipment):
        super().__init__(village.player_sprites, village.all_sprites, village.collide_sprites, village.attack_sprites)
        pos = random.choice([(village_size // 4, village_size // 2),
                             (village_size // 4 * 3, village_size // 2),
                             (village_size // 2, village_size // 4),
                             (village_size // 2, village_size // 4 * 3)])

        # Переменные, основные
        self.attributes = PlayerAttributes.init()
        self.image = pygame.transform.scale(load_image('hero.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * GAME_CELL_SIZE
        self.rect.y = int(pos[1]) * GAME_CELL_SIZE

        # Переменные, атака
        self.is_attack = [False, False]
        self.angle_attack_range = None
        self.angle_attack_move = None
        self.count_attack = -1

        # Инвентари
        self.inventory = inventory
        self.equipment_inventory = equipment

        # self.player_equipment = {}
        # i = 0
        # for item in ["sword", "helmet", "armor", "pants", "boots"]:
        #     slot = self.equipment_inventory.slots[0][i]
        #     if slot.item.ID != -1:
        #         self.player_equipment[item] = slot
        #     else:
        #         self.player_equipment[item] = None
        #     i += 1
        
        # self.apply_modifiers()

        for slot in self.equipment_inventory.slots[0]:
            self.apply_modifiers(slot.item)

        # Прочие переменные
        self.state = PlayerStates.Normal
        self.directions = {(0, -STEP): False, (-STEP, 0): False,
                           (0, STEP): False, (STEP, 0): False}
        self.is_dmg = False

    def apply_modifiers(self, item):
        if item.TYPE == ItemType.Weapon or item.TYPE == ItemType.Equipment:
            for buff in item.buffs:
                self.attributes[buff.affected_attribute].current_value += buff.value
            if item.TYPE == ItemType.Weapon:
                self.attributes[Attributes.Damage].current_value += item.damage.value

    def damage(self, dmg):
        if self.state == PlayerStates.Normal:
            print(10)
            self.is_dmg = True
            self.attributes[Attributes.Health].current_value -= dmg
            if self.attributes[Attributes.Health].current_value < 1:
                self.state = PlayerStates.Dead
                self.attributes[Attributes.Health].current_value = AttributeValue()
        return self.state

    def move_player(self, direction, village):
        # Проверка нужно ли идти в данную сторону
        if direction[1]:
            # Движение в эту сторону
            x = direction[0][0] * self.attributes[Attributes.Move_Speed].current_value
            y = direction[0][1] * self.attributes[Attributes.Move_Speed].current_value
            self.rect = self.rect.move(x, y)
            # Если герой врезался во что то, то возвращаем назад
            collide = False
            for sprite in village.collide_sprites:
                if pygame.sprite.collide_mask(self, sprite) and sprite != self:
                    collide = True
                    break
            if collide:
                self.rect = self.rect.move(-x, -y)

    def attack(self, village):
        # Очистка
        for sword in village.sword_sprites:
            village.sword_sprites.remove(sword)
        self.weapon = Weapon(village, 'sword')
        # Обычная атака
        if self.is_attack[0]:
            size_step_attack = 8
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = \
                    search_angle(Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                                 Vector2(self.rect.x, self.rect.y))[0] + 40, \
                    search_angle(Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                                 Vector2(self.rect.x, self.rect.y))[1] + MIN_COE * 40
                self.count_attack = 10
            # Отрисовка и шаг
            step_and_draw_attack(self, size_step_attack)
            # Атака
            self.weapon.attack(self.attributes[Attributes.Damage].current_value, village)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack[0] = False
                for sprite in village.attack_sprites:
                    sprite.is_dmg = False
        # Круговая атака
        elif self.is_attack[1]:
            size_step_attack = 12
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = \
                    search_angle(Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]),
                                 Vector2(self.rect.x, self.rect.y))
                self.count_attack = 360 // size_step_attack
            # Отрисовка и шаг
            step_and_draw_attack(self, size_step_attack)
            # Атака
            self.weapon.attack(self.attributes[Attributes.Damage].current_value // 2, village)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack[1] = False
                for sprite in village.attack_sprites:
                    sprite.is_dmg = False
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
