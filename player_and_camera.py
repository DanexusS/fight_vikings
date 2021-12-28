import pygame
import random
import threading
import time
import os

# Константы
CELL_SIZE = 40
STEP = 4


def load_image(name):
    fullname = os.path.join('images/', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 6, n // 2), (n // 6 * 5, n // 2), (n // 2, n // 6), (n // 2, n // 6 * 5)])
        # Переменные
        self.hp = 10
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('hero.png'), (CELL_SIZE, CELL_SIZE))
        self.sword = pygame.transform.scale(load_image('sword.png'), (CELL_SIZE, CELL_SIZE))
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
    '''
    def attack(self, screen):
        surf = pygame.Surface((100, 100))
        # for i in range(1, 361):
        screen.blit(surf, (self.rect.x - 30, self.rect.y - 30))
        img = pygame.transform.rotate(self.sword, 0)
        surf.blit(img, self.rect)

        pygame.display.flip()
        pygame.time.delay(1)
    '''
    def update(self, event, screen):
        '''
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                t = threading.Thread(target=self.attack(screen))
                t.daemon = True
                t.start()
        '''
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
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
