import pygame
import math

from constants import *
from functions import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, other):
        super().__init__(other.sword_sprites)
        # Переменные
        self.image = pygame.transform.rotate(pygame.transform.scale(load_image('sword.png'), (PLAYER_SIZE - 10, PLAYER_SIZE - 10)), 180)
        self.rect = self.image.get_rect()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        return angle

    def attack(self, dmg, other):
        # Если соприкосаеться с объектом - удар
        objs_collide = []
        for sprite in other.collide_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                obj = sprite
                objs_collide.append(obj)
                # Бьёт 1 раз
                if not obj.is_dmg:
                    status = obj.damage(dmg)
                    if obj.__class__.__name__ == 'Enemy' and status == 'destroed':
                        obj.kill()
                        other.enemies.remove(obj)
        # Перезагрузка удара
        for sprite in other.collide_sprites:
            if sprite not in objs_collide:
                sprite.is_dmg = False


class Hero(pygame.sprite.Sprite):
    def __init__(self, other, n):
        super().__init__(other.player_sprites, other.all_sprites)
        pos = random.choice([(n // 4, n // 2), (n // 4 * 3, n // 2), (n // 2, n // 4), (n // 2, n // 4 * 3)])
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
        self.hp = 200
        self.status = 'normal'
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

    def search_angle(self):
        # Переменные
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle_move = 0
        # Формула
        sqrt1 = math.sqrt((mouse_x - PLAYER_CENTER_X + 1) * (mouse_x - PLAYER_CENTER_X + 1) + (mouse_y - PLAYER_CENTER_Y + 1) * (mouse_y - PLAYER_CENTER_Y + 1))
        sqrt2 = math.sqrt(0 * 0 + 10 * 10)
        angle = round(-(90 - math.acos(math.cos(((mouse_x - PLAYER_CENTER_X) * 0 + (mouse_y - PLAYER_CENTER_Y) * 10) / ((sqrt1 * sqrt2) + 1))) * 100))
        # Выравнивание градуса угла
        if mouse_x <= PLAYER_CENTER_X and mouse_y <= PLAYER_CENTER_Y:
            angle = (270 - angle) - 80
            angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
        elif mouse_x <= PLAYER_CENTER_X and mouse_y >= PLAYER_CENTER_Y:
            angle = angle - 10
            angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
        elif mouse_x >= PLAYER_CENTER_X and mouse_y <= PLAYER_CENTER_Y:
            angle -= 190
            angle_move = MAX_COEFF - (MIN_COEFF * abs(angle // STEP_ANGLE))
        elif mouse_x >= PLAYER_CENTER_X and mouse_y >= PLAYER_CENTER_Y:
            angle = (90 - angle) - 80
            angle_move = MIN_COEFF * abs(angle // STEP_ANGLE)
        return [angle, angle_move]

    def step_and_draw_attack(self, size_step_attack):
        r = 45
        # Отрисовка
        self.weapon.image = pygame.transform.rotate(self.weapon.image, self.angle_attack_range)
        self.weapon.rect = self.weapon.image.get_rect()
        self.weapon.rect.x = PLAYER_CENTER_X + r * math.sin(self.angle_attack_move)
        self.weapon.rect.y = PLAYER_CENTER_Y + r * math.cos(self.angle_attack_move)
        # Шаг
        self.angle_attack_range -= STEP_ANGLE * size_step_attack
        self.angle_attack_move -= MIN_COEFF * size_step_attack
        self.count_attack -= 1

    def attack(self, other):
        # Очистка
        for sword in other.sword_sprites:
            other.sword_sprites.remove(sword)
        self.weapon = Weapon(other)
        # Обычная атака
        if self.is_attack[0]:
            size_step_attack = 8
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = self.search_angle()[0] + 40, self.search_angle()[1] + MIN_COEFF * 40
                self.count_attack = 10
            # Отрисовка и шаг
            self.step_and_draw_attack(size_step_attack)
            # Атака
            self.weapon.attack(8, other)
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
            self.weapon.attack(4, other)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack[1] = False
        else:
            # Если герой не атакует, то меч удалить
            self.weapon.kill()

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
        super().__init__(other.enemies_sprites, other.all_sprites, other.collide_sprites)
        # Переменные
        self.hp = 80
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

    def obstacle_avoidance(self):
        # Проверка на возможность столкновения
        availability = {'left': True, 'right': True, 'up': True, 'down': True}
        for elem in [self.rect.move((STEP - 1), 0), self.rect.move(-(STEP - 1), 0)]:
            old_rect = self.rect
            self.rect = elem
            for sprite in other.collide_sprites:
                if pygame.sprite.collide_mask(self, sprite):
                    obj = sprite

    def update(self, player):
        if 100 < self.rect.x < WIDTH - 100 and 50 < self.rect.y < HEIGHT - 50:
            x = WIDTH // 2 - PLAYER_SIZE // 2
            y = HEIGHT // 2 - PLAYER_SIZE // 2
            # Ходьба по маршруту
            if self.rect.x <= x:
                self.rect = self.rect.move((STEP - 1), 0)
            if self.rect.x >= x:
                self.rect = self.rect.move(-(STEP - 1), 0)
            if self.rect.y <= y:
                self.rect = self.rect.move(0, (STEP - 1))
            if self.rect.y >= y:
                self.rect = self.rect.move(0, -(STEP - 1))
            # self.obstacle_avoidance()


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target, width, height):
        self.dx = -(target.rect.x - width // 2) - PLAYER_SIZE // 2
        self.dy = -(target.rect.y - height // 2) - PLAYER_SIZE // 2
