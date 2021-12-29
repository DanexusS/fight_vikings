import pygame
import math
import os

from constants import *


def load_image(name):
    fullname = os.path.join('images/', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 4, n // 2), (n // 4 * 3, n // 2), (n // 2, n // 4), (n // 2, n // 4 * 3)])
        # Переменные
        self.hp = 10
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('hero.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.sword = pygame.transform.rotate(pygame.transform.scale(load_image('sword.png'), (PLAYER_SIZE, PLAYER_SIZE)), 180)
        self.angle_sword = 0
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

    def attack(self, screen, other):
        if 360 > self.angle_sword > 0:
            r = 45
            sword_img = pygame.transform.rotate(self.sword, self.angle_sword)
            screen.blit(sword_img, (WIDTH // 2 + r * math.sin(self.angle_move), HEIGHT // 2 + r * math.cos(self.angle_move)))
            if pygame.sprite.spritecollideany(self, other.houses_sprites):
                # Сделать удар по домам
                pass
            pygame.display.flip()
            self.angle_sword += 15
            self.angle_move += 0.26
        if self.angle_sword >= 360 or self.angle_sword <= 0:
            self.angle_sword = 0
            self.angle_move = 0

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.angle_sword == 0:
                    self.angle_sword = 5

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
