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
    def __init__(self, village, pos):
        super().__init__(village.enemies_sprites, village.all_sprites, village.collide_sprites, village.attack_sprites)
        # Переменные, основные
        self.image = pygame.transform.scale(load_image('enemy.png'), (PLAYER_SIZE, PLAYER_SIZE))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0]) + CELL_SIZE // 2 - PLAYER_SIZE // 2
        self.rect.y = int(pos[1]) + CELL_SIZE // 2 - PLAYER_SIZE // 2
        # Переменные, прочие
        self.pos = [self.rect.x, self.rect.y]
        self.hp = 80
        self.status = 'normal'
        self.is_dmg = False

    def damage(self, dmg):
        if self.status == 'normal':
            self.is_dmg = True
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroyed'
                self.hp = 0
        return self.status

    def back_move(self, other, x_move, y_move):
        for sprite in other.collide_sprites:
            if pygame.sprite.collide_mask(self, sprite) and sprite != self:
                self.rect = self.rect.move(-x_move, -y_move)
                break

    def update(self, other):
        if 100 < self.rect.x < WIDTH - 100 and 50 < self.rect.y < HEIGHT - 50:
            x = WIDTH // 2 - PLAYER_SIZE // 2
            y = HEIGHT // 2 - PLAYER_SIZE // 2
        elif self.rect.x != self.pos[0] or self.rect.y != self.pos[1]:
            x = self.pos[0]
            y = self.pos[1]
        else:
            return
        # Ходьба к герою
        if self.rect.x <= x:
            self.rect = self.rect.move((STEP - 1), 0)
            self.back_move(other, (STEP - 1), 0)
        if self.rect.x >= x:
            self.rect = self.rect.move(-(STEP - 1), 0)
            self.back_move(other, -(STEP - 1), 0)
        if self.rect.y <= y:
            self.rect = self.rect.move(0, (STEP - 1))
            self.back_move(other, 0, (STEP - 1))
        if self.rect.y >= y:
            self.rect = self.rect.move(0, -(STEP - 1))
            self.back_move(other, 0, -(STEP - 1))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
        if obj.__class__.__name__ == 'Enemy':
            obj.pos[0] += self.dx
            obj.pos[1] += self.dy

    def update(self, target, width, height):
        self.dx = -(target.rect.x - width // 2) - PLAYER_SIZE // 2
        self.dy = -(target.rect.y - height // 2) - PLAYER_SIZE // 2
