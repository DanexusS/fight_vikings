from main_functions import *
from weapon_class import Weapon


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
        self.obstacle = [False, None]
        self.move_vectors = {'right': Vector2((STEP - 1), 0), 'left': Vector2(-(STEP - 1), 0),
                             'down': Vector2(0, (STEP - 1)), 'up': Vector2(0, -(STEP - 1))}

        # Переменные, атака
        self.is_attack = False
        self.angle_attack_range = None
        self.angle_attack_move = None
        self.count_attack = -1

    def damage(self, dmg):
        if self.status == 'normal':
            self.is_dmg = True
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroyed'
                self.hp = 0
        return self.status

    def attack(self, village):
        # Очистка
        for sword in village.sword_sprites:
            village.sword_sprites.remove(sword)
        self.weapon = Weapon(village, 'sword')
        # Обычная атака
        if self.is_attack:
            size_step_attack = 8
            # Начало цикла атаки
            if self.count_attack == -1:
                self.angle_attack_range, self.angle_attack_move = \
                    search_angle(Vector2(self.rect.x, self.rect.y), PLAYER_CENTER)[0] + 40, \
                    search_angle(Vector2(self.rect.x, self.rect.y), PLAYER_CENTER)[1] + MIN_COE * 40
                self.count_attack = 10
            # Отрисовка и шаг
            step_and_draw_attack(self, size_step_attack)
            # Атака
            self.weapon.attack(10, village)
            # Конец цикла атаки
            if self.count_attack == 0:
                self.count_attack = -1
                self.is_attack = False
                for sprite in village.attack_sprites:
                    sprite.is_dmg = False

    def check_collide(self, village, posx, posy, move=False, only_house=False):
        c = 1
        distance = math.sqrt((PLAYER_CENTER.x - self.rect.x) ** 2 + (PLAYER_CENTER.y - self.rect.y) ** 2)
        if move:
            self.rect = self.rect.move(posx * c, posy * c)
        for sprite in village.collide_sprites:
            if pygame.sprite.collide_mask(self, sprite) and \
                    (sprite != self and
                     (not only_house or (sprite.__class__.__name__ not in ['Enemy', 'Hero'] and
                                         distance > (PLAYER_SIZE + 10) * 3) or distance < (PLAYER_SIZE + 10) * 3)):
                self.rect = self.rect.move(-posx * c, -posy * c)
                return sprite
        if move:
            self.rect = self.rect.move(-posx * c, -posy * c)
        return False

    def check_avoidance(self, village, x_move, y_move):
        sprite = self.check_collide(village, x_move, y_move)
        if sprite:
            left_or_right = random.randint(0, 1)
            distance = math.sqrt((PLAYER_CENTER.x - self.rect.x) ** 2 + (PLAYER_CENTER.y - self.rect.y) ** 2)
            if not self.obstacle[0] and \
                    ((distance > (PLAYER_SIZE + 10) * 3 and
                      sprite.__class__.__name__ not in ['Enemy', 'Hero']) or
                     ((PLAYER_SIZE + 10) < distance < (PLAYER_SIZE + 10) * 3 and
                      sprite.__class__.__name__ == 'Enemy')):
                if (self.check_collide(village, self.move_vectors['up'].x, self.move_vectors['up'].y,
                                       True) or
                      self.check_collide(village, self.move_vectors['down'].x, self.move_vectors['down'].y,
                                         True)) and \
                        (PLAYER_CENTER.x - PLAYER_SIZE < self.rect.x < PLAYER_CENTER.x + PLAYER_SIZE):
                    if left_or_right == 1:
                        self.obstacle = [True, 'right']
                    else:
                        self.obstacle = [True, 'left']
                elif (self.check_collide(village, self.move_vectors['left'].x, self.move_vectors['left'].y,
                                         True) or
                      self.check_collide(village, self.move_vectors['right'].x, self.move_vectors['right'].y,
                                         True)) and \
                        (PLAYER_CENTER.y - PLAYER_SIZE < self.rect.y < PLAYER_CENTER.y + PLAYER_SIZE):
                    if left_or_right == 1:
                        self.obstacle = [True, 'down']
                    else:
                        self.obstacle = [True, 'up']

    def update(self, village):
        distance = math.sqrt((PLAYER_CENTER.x - self.rect.x) ** 2 + (PLAYER_CENTER.y - self.rect.y) ** 2)
        if distance < 500:
            x = PLAYER_CENTER.x
            y = PLAYER_CENTER.y
        elif self.rect.x != self.pos[0] or self.rect.y != self.pos[1]:
            x = self.pos[0]
            y = self.pos[1]
        else:
            return
        if self.obstacle[0]:
            # Обход препятствия если требуеться
            self.rect = self.rect.move(self.move_vectors[self.obstacle[1]].x, self.move_vectors[self.obstacle[1]].y)
            if self.check_collide(village, self.move_vectors[self.obstacle[1]].x,
                                  self.move_vectors[self.obstacle[1]].y):
                if self.obstacle[1] == 'right':
                    self.obstacle[1] = 'left'
                if self.obstacle[1] == 'left':
                    self.obstacle[1] = 'right'
                if self.obstacle[1] == 'down':
                    self.obstacle[1] = 'up'
                if self.obstacle[1] == 'up':
                    self.obstacle[1] = 'down'
            if (not self.check_collide(village, self.move_vectors['up'].x, self.move_vectors['up'].y,
                                       True, True) and \
                    not self.check_collide(village, self.move_vectors['down'].x, self.move_vectors['down'].y,
                                           True, True) and
                    not self.check_collide(village, self.move_vectors['left'].x, self.move_vectors['left'].y,
                                           True, True) and
                    not self.check_collide(village, self.move_vectors['right'].x, self.move_vectors['right'].y,
                                           True, True)):
                self.rect = self.rect.move(self.move_vectors[self.obstacle[1]].x, self.move_vectors[self.obstacle[1]].y)
                self.check_collide(village, self.move_vectors[self.obstacle[1]].x,
                                   self.move_vectors[self.obstacle[1]].y)
                self.obstacle = [False, None]
        else:
            # Ходьба к герою
            if self.rect.x <= x:
                self.rect = self.rect.move(self.move_vectors['right'].x, self.move_vectors['right'].y)
                self.check_avoidance(village, self.move_vectors['right'].x, self.move_vectors['right'].y)
            if self.rect.x >= x:
                self.rect = self.rect.move(self.move_vectors['left'].x, self.move_vectors['left'].y)
                self.check_avoidance(village, self.move_vectors['left'].x, self.move_vectors['left'].y)
            if self.rect.y <= y:
                self.rect = self.rect.move(self.move_vectors['down'].x, self.move_vectors['down'].y)
                self.check_avoidance(village, self.move_vectors['down'].x, self.move_vectors['down'].y)
            if self.rect.y >= y:
                self.rect = self.rect.move(self.move_vectors['up'].x, self.move_vectors['up'].y)
                self.check_avoidance(village, self.move_vectors['up'].x, self.move_vectors['up'].y)


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
