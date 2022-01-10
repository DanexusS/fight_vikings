import pygame
import math

from constants import *
from functions import *


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.player_sprites, other.all_sprites)
        # Переменные
        self.hp = 50
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('enemy.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) * CELL_SIZE
        self.rect.y = int(pos[1]) * CELL_SIZE

    def damage(self, dmg):
        if self.status == 'normal':
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
        return self.status

    def attack(self, other):
        pass

    def update(self, player):
        distance = math.sqrt((self.rect.x - player.rect.x) ** 2 + (self.rect.x - player.rect.x) ** 2)
        if distance < 1000:
