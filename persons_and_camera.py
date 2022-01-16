import math

from main_functions import *


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
                    if obj.__class__.__name__ == 'Enemy' and status == 'destroyed':
                        obj.kill()
                        other.enemies.remove(obj)
        # Перезагрузка удара
        for sprite in other.collide_sprites:
            if sprite not in objs_collide:
                sprite.is_dmg = False


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
                self.status = 'destroyed'
                self.hp = 0
        return self.status

    def obstacle_avoidance(self, other):
        # Проверка на возможность столкновения
        c = 5
        move = [self.rect.move((STEP - 1) * c, 0), self.rect.move(-(STEP - 1) * c, 0),
                self.rect.move(0, (STEP - 1) * c), self.rect.move(0, -(STEP - 1) * c)]
        availability = {'left': True, 'right': True, 'up': True, 'down': True}
        for i, elem in enumerate(move):
            old_rect = self.rect.copy()
            self.rect = elem
            for sprite in other.collide_sprites:
                if pygame.sprite.collide_mask(self, sprite) and sprite != self:
                    availability[list(availability.keys())[i]] = False
            self.rect = old_rect
        return availability

    def update(self, other):
        if 100 < self.rect.x < WIDTH - 100 and 50 < self.rect.y < HEIGHT - 50:
            x = WIDTH // 2 - PLAYER_SIZE // 2
            y = HEIGHT // 2 - PLAYER_SIZE // 2
            # Переменная с возможными путями =================== Доделать, но лучше переделать
            '''
            availability = self.obstacle_avoidance(other)
            # Если есть тупики, то обход
            if not any(list(availability.values())):
                pass
            elif not availability['left'] or not availability['right']:
                if availability['up'] and (not availability['down'] or (abs(self.rect.y - y) > CELL_SIZE and self.rect.y - (STEP - 1) - y > y - (self.rect.y + (STEP - 1)))):
                    self.rect = self.rect.move(0, -(STEP - 1))
                elif availability['down']:
                    self.rect = self.rect.move(0, (STEP - 1))
            elif not availability['up'] or not availability['down']:
                if availability['left'] and (not availability['right'] or (abs(self.rect.x - x) > CELL_SIZE and self.rect.x - (STEP - 1) - x > x - (self.rect.x + (STEP - 1)))):
                    self.rect = self.rect.move(-(STEP - 1), 0)
                elif availability['right']:
                    self.rect = self.rect.move((STEP - 1), 0)
            else:
            '''
            # Ходьба к герою
            if self.rect.x <= x:
                self.rect = self.rect.move((STEP - 1), 0)
            if self.rect.x >= x:
                self.rect = self.rect.move(-(STEP - 1), 0)
            if self.rect.y <= y:
                self.rect = self.rect.move(0, (STEP - 1))
            if self.rect.y >= y:
                self.rect = self.rect.move(0, -(STEP - 1))


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
