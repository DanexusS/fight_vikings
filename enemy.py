import pygame
import math

from constants import *
from functions import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 4, n // 2), (n // 4 * 3, n // 2), (n // 2, n // 4), (n // 2, n // 4 * 3)])
        # Переменные
        self.hp = 10
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('enemy.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.attack_default = True
        self.angle_attack_range = 0
        self.angle_move = 0
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * CELL_SIZE
        self.rect.y = int(pos[1]) * CELL_SIZE
        self.run = 1

    def damage(self, dmg):
        if self.status == 'normal':
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
            return self.status
        return None

    def move_player(self, direction, other):
        pass

    def attack(self, other):
        pass

    def update(self, event):
        pass
