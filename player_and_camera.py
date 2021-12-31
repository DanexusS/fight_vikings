import pygame
import math
import os

from constants import *


def load_image(name):
    fullname = os.path.join('images/', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class Sword(pygame.sprite.Sprite):
    def __init__(self, other):
        super().__init__(other.sword_sprites, other.all_sprites)
        self.image = pygame.transform.rotate(pygame.transform.scale(load_image('sword.png'), (PLAYER_SIZE, PLAYER_SIZE)), 180)
        self.rect = self.image.get_rect()

    def attack(self, group):
        if pygame.sprite.spritecollideany(self, group):
            pygame.sprite.spritecollideany(self, group).damage(1)


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 4, n // 2), (n // 4 * 3, n // 2), (n // 2, n // 4), (n // 2, n // 4 * 3)])
        # Переменные
        self.hp = 10
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('hero.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.angle_attack_range = 0
        self.attack_default = 0
        self.angle_move = 0
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * CELL_SIZE
        self.rect.y = int(pos[1]) * CELL_SIZE
        self.directions = {(0, -STEP): False, (-STEP, 0): False, (0, STEP): False, (STEP, 0): False}
        self.run = 1

    def damage(self, dmg):
        if self.hp > 0:
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
            return self.status
        return None

    def move_player(self, direction, other):
        if direction[1]:
            x = direction[0][0] * self.run
            y = direction[0][1] * self.run
            self.rect = self.rect.move(x, y)
            if pygame.sprite.spritecollideany(self, other.trees_sprites) or \
                    (pygame.sprite.spritecollideany(self, other.houses_sprites) or
                     pygame.sprite.spritecollideany(self, other.townhall_sprites)):
                self.rect = self.rect.move(-x, -y)

    def attack(self, screen, other, pos):
        self.sword = Sword(other)
        # Обычная атака
        if bool(self.attack_default):
            # Переменные
            r = 45
            x = WIDTH // 2
            y = HEIGHT // 2
            # Формула
            sqrt1 = math.sqrt((pos[0] - x) * (pos[0] - x) + (pos[1] - y) * (pos[1] - y))
            sqrt2 = math.sqrt(0 * 0 + 10 * 10)
            angle = round(-(90 - math.acos(math.cos(((pos[0] - x) * 0 + (pos[1] - y) * 10) / (sqrt1 * sqrt2))) * 100))
            # Выравнивание градуса угла
            if pos[0] <= WIDTH // 2 and pos[1] <= HEIGHT // 2:
                angle = 270 - angle - 90
                angle_move = 0.26 * abs(angle // 15)
            elif pos[0] <= WIDTH // 2 and pos[1] >= HEIGHT // 2:
                angle_move = (0.26 * (360 // 15)) - (0.26 * abs(angle // 15))
            elif pos[0] >= WIDTH // 2 and pos[1] <= HEIGHT // 2:
                angle -= 180
                angle_move = (0.26 * (360 // 15)) - (0.26 * abs(angle // 15))
            elif pos[0] >= WIDTH // 2 and pos[1] >= HEIGHT // 2:
                angle = 90 - angle - 90
                angle_move = 0.26 * abs(angle // 15)
            # Отрисовка
            self.sword.image = pygame.transform.rotate(self.sword.image, angle)
            self.sword.rect = self.sword.image.get_rect()
            self.sword.rect.x = x + r * math.sin(angle_move)
            self.sword.rect.y = y + r * math.cos(angle_move)
            other.sword_sprites.draw(screen)
            self.attack_default -= 1
            # Проверка на атаку \/ 1 раз
            if self.attack_default == 10:
                self.sword.attack(other.houses_sprites)
                self.sword.attack(other.townhall_sprites)
        # Круговая атака
        elif bool(self.angle_attack_range):
            # Переменные
            r = 45
            # Отрисовка
            self.sword.image = pygame.transform.rotate(self.sword.image, self.angle_attack_range)
            self.sword.rect = self.sword.image.get_rect()
            self.sword.rect.x = WIDTH // 2 + r * math.sin(self.angle_move)
            self.sword.rect.y = HEIGHT // 2 + r * math.cos(self.angle_move)
            other.sword_sprites.draw(screen)
            self.angle_attack_range -= 15
            self.angle_move -= 0.26
            # Проверка на атаку
            self.sword.attack(other.houses_sprites)
            self.sword.attack(other.townhall_sprites)

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.attack_default == 0:
                    self.attack_default = 20
            if event.button == 3:
                if self.angle_attack_range == 0:
                    self.angle_attack_range = 360
                    self.angle_move = 0.26 * (360 // 15)

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
