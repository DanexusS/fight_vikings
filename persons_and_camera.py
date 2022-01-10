import pygame
import math

from constants import *
from functions import *


class Sword(pygame.sprite.Sprite):
    def __init__(self, other):
        super().__init__(other.sword_sprites)
        # Переменные
        self.image = pygame.transform.rotate(pygame.transform.scale(load_image('sword.png'), (PLAYER_SIZE, PLAYER_SIZE)), 180)
        self.rect = self.image.get_rect()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        return angle

    def attack(self, dmg, other):
        # Если соприкосаеться с объектом - удар
        for group in [other.houses_sprites, other.townhall_sprites, other.enemies_sprites]:
            obj = None
            for sprite in group:
                if pygame.sprite.collide_mask(self, sprite):
                    obj = sprite
                    print(obj.__class__.__name__)
                    break
            if obj:
                # Бьёт 1 раз
                if not obj.is_dmg:
                    status = obj.damage(dmg)
                    if obj.__class__.__name__ == 'Enemy' and status == 'destroed':
                        other.enemies_sprites.remove(obj)
                        other.enemies.remove(obj)

            else:
                # Перезагрузка удара
                for sprite in group:
                    sprite.is_dmg = False


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 4, n // 2), (n // 4 * 3, n // 2), (n // 2, n // 4), (n // 2, n // 4 * 3)])
        # Переменные
        self.hp = 100
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('hero.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.attack_default = True
        self.angle_attack_range = 0
        self.angle_move = 0
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * CELL_SIZE
        self.rect.y = int(pos[1]) * CELL_SIZE
        self.directions = {(0, -STEP): False, (-STEP, 0): False, (0, STEP): False, (STEP, 0): False}
        self.run = 1

    def damage(self, dmg):
        if self.status == 'normal':
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
        return self.status

    def move_player(self, direction, other):
        # Проверка нужно ли идти в данную сторону
        if direction[1]:
            # Движение в эту сторону
            x = direction[0][0] * self.run
            y = direction[0][1] * self.run
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

    def attack(self, other):
        # Очистка
        for sword in other.sword_sprites:
            other.sword_sprites.remove(sword)
        self.sword = Sword(other)
        # Обычная атака
        if bool(self.attack_default):
            # Переменные
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dmg = 8
            r = 45
            x = WIDTH // 2
            y = HEIGHT // 2
            # Формула
            sqrt1 = math.sqrt((mouse_x - x + 1) * (mouse_x - x + 1) + (mouse_y - y + 1) * (mouse_y - y + 1))
            sqrt2 = math.sqrt(0 * 0 + 10 * 10)
            angle = round(-(90 - math.acos(math.cos(((mouse_x - x) * 0 + (mouse_y - y) * 10) / ((sqrt1 * sqrt2) + 1))) * 100))
            # Выравнивание градуса угла
            if mouse_x <= x and mouse_y <= y:
                angle = (270 - angle) - 80
                angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
            elif mouse_x <= x and mouse_y >= y:
                angle = angle - 10
                angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
            elif mouse_x >= x and mouse_y <= y:
                angle -= 190
                angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
            elif mouse_x >= x and mouse_y >= y:
                angle = (90 - angle) - 80
                angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
            # Отрисовка
            self.sword.image = pygame.transform.rotate(self.sword.image, angle)
            self.sword.rect = self.sword.image.get_rect()
            self.sword.rect.x = x + r * math.sin(angle_move)
            self.sword.rect.y = y + r * math.cos(angle_move)
            # Проверка на атаку
            self.sword.attack(dmg, other)
        # Круговая атака
        elif bool(self.angle_attack_range):
            # Переменные
            dmg = 4
            r = 45
            step_angle = 15
            step_coeff = 0.26
            # Отрисовка
            self.sword.image = pygame.transform.rotate(self.sword.image, self.angle_attack_range)
            self.sword.rect = self.sword.image.get_rect()
            self.sword.rect.x = WIDTH // 2 + r * math.sin(self.angle_move)
            self.sword.rect.y = HEIGHT // 2 + r * math.cos(self.angle_move)
            self.angle_attack_range -= step_angle
            self.angle_move -= step_coeff
            # Проверка на атаку
            self.sword.attack(dmg, other)
            if self.angle_attack_range == 0:
                self.attack_default = True
        else:
            # Если герой не атакует, то меч за экраном
            self.sword.rect.x = -100
            self.sword.rect.y = -100

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if self.angle_attack_range == 0:
                    self.angle_attack_range = 360
                    self.angle_move = 0.26 * (360 // 15)
                    self.attack_default = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.run = 2

            if event.key == pygame.K_w:
                self.directions[(0, -STEP)] = True
            if event.key == pygame.K_a:
                self.directions[(-STEP, 0)] = True
            if event.key == pygame.K_s:
                self.directions[(0, STEP)] = True
            if event.key == pygame.K_d:
                self.directions[(STEP, 0)] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.run = 1

            if event.key == pygame.K_w:
                self.directions[(0, -STEP)] = False
            if event.key == pygame.K_a:
                self.directions[(-STEP, 0)] = False
            if event.key == pygame.K_s:
                self.directions[(0, STEP)] = False
            if event.key == pygame.K_d:
                self.directions[(STEP, 0)] = False




class Enemy(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.all_sprites)
        # Переменные
        self.hp = 50
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('enemy.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) + CELL_SIZE // 2 - PLAYER_SIZE // 2
        self.rect.y = int(pos[1]) + CELL_SIZE // 2 - PLAYER_SIZE // 2
        self.is_dmg = False

    def damage(self, dmg):
        if self.status == 'normal':
            self.is_dmg = True
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
        return self.status

    def update(self, player):
        self.rect = self.rect.move(0, 0)
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.x - player.rect.x) ** 2)
        if distance < 1000:
            x = WIDTH // 2
            y = HEIGHT // 2
            # Формула
            sqrt1 = math.sqrt((self.rect.x - x + 1) * (self.rect.x - x + 1) + (self.rect.y - y + 1) * (self.rect.y - y + 1))
            sqrt2 = math.sqrt(0 * 0 + 10 * 10)
            angle = round(-(90 - math.acos(math.cos(((self.rect.x - x) * 0 + (self.rect.y - y) * 10) / ((sqrt1 * sqrt2) + 1))) * 100))
            # Выравнивание градуса угла
            if self.rect.x <= x and self.rect.y <= y:
                angle = (270 - angle) - 80
                angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
            elif self.rect.x <= x and self.rect.y >= y:
                angle = angle - 10
                angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
            elif self.rect.x >= x and self.rect.y <= y:
                angle -= 190
                angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
            elif self.rect.x >= x and self.rect.y >= y:
                angle = (90 - angle) - 80
                angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
            # Отрисовка
            self.rect.x = 0
            self.rect.y = 0


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, width, height):
        self.dx = -(target.rect.x - width // 2) + 5
        self.dy = -(target.rect.y - height // 2) + 5
