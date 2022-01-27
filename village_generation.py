"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import persons_and_camera
from general_stuff import *


class House(pygame.sprite.Sprite):
    def __init__(self, village, pos):
        super().__init__(village.houses_sprites, village.all_sprites, village.collide_sprites, village.attack_sprites)
        # Переменные
        self.hp = 100
        self.status = 'normal'
        self.image = size_img('house.png')
        self.mask = pygame.mask.from_surface(size_img('mask_house.png'))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])
        self.is_dmg = False
        self.village = village

    def damage(self, dmg):
        if self.status == 'normal':
            self.is_dmg = True
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.image = size_img('housedie.png')
                self.village.gold += random.randint(2, 4)
                self.village.tree += random.randint(3, 5)
                self.village.metal += random.randint(1, 3)
        return self.status


class TownHall(pygame.sprite.Sprite):
    def __init__(self, village, pos, angle):
        super().__init__(village.townhall_sprites, village.all_sprites, village.collide_sprites, village.attack_sprites)
        # Переменные
        x, y = pos
        self.hp = 300
        self.status = 'normal'
        self.angle = angle
        # Установка картинок
        self.image = size_img(f"townhall{self.angle}.png", 3)
        self.mask = pygame.mask.from_surface(size_img(f"mask_townhall{self.angle}.png", 3))
        if self.angle == 0:
            y -= GAME_CELL_SIZE * 0.2
        elif self.angle == 1:
            x -= GAME_CELL_SIZE
            y -= GAME_CELL_SIZE * 0.2
        elif self.angle == 2:
            y -= GAME_CELL_SIZE * 2
        elif self.angle == 3:
            y -= GAME_CELL_SIZE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_dmg = False

        self.village = village

    def damage(self, dmg):
        if self.status == 'normal':
            self.is_dmg = True
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.image = size_img(f"townhall{self.angle}.png", 3)
                self.village.gold += random.randint(15, 40)
                self.village.tree += random.randint(10, 40)
                self.village.metal += random.randint(5, 30)
        return self.status


class Road(pygame.sprite.Sprite):
    def __init__(self, village, pos):
        super().__init__(village.all_sprites)
        # Переменные
        self.image = size_img('road.png')
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


class Grass(pygame.sprite.Sprite):
    def __init__(self, village, pos):
        super().__init__(village.all_sprites)
        # Переменные
        self.image = size_img('grass.png')
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


class Tree(pygame.sprite.Sprite):
    def __init__(self, village, pos):
        super().__init__(village.trees_sprites, village.all_sprites, village.collide_sprites)
        # Переменные
        self.image = size_img('tree.png')
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


# =======================================================================================================
class Village:
    def __init__(self, width, height):
        # Переменные поля и клеток
        self.width = width
        self.height = height
        self.cell_size = GAME_CELL_SIZE
        self.left = EMPTY_N * GAME_CELL_SIZE
        self.top = EMPTY_N * GAME_CELL_SIZE

        # Общие группы
        self.all_sprites = pygame.sprite.Group()
        self.collide_sprites = pygame.sprite.Group()
        # Определённые группы
        self.houses_sprites = pygame.sprite.Group()
        self.townhall_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.sword_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()

        self.Town_Hall = ''

        self.gold = 0
        self.tree = 0
        self.metal = 0

        self.enemies = []
        # Пустые клетки вокруг деревни
        for i in range(-MAP_SIZE, self.height + MAP_SIZE * 2):
            for j in range(-MAP_SIZE, self.width + MAP_SIZE * 2):
                x = j * self.cell_size
                y = i * self.cell_size
                Grass(self, (x, y))
        # Матрица
        self.board = []
        for i in range(self.height):
            self.board.append({})
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                self.board[i][f"{x} {y}"] = Grass(self, (x, y))
        # Генерация
        self.generation()

    def set_view(self, left, top, cell_size=GAME_CELL_SIZE):
        # Установка новых значений
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generation()

    def add_roads(self, x, y, x_or_y):
        for i in range(self.height):
            for j in range(self.width):
                x1 = self.left + j * self.cell_size
                y1 = self.top + i * self.cell_size
                if (x_or_y == 'y' and y1 == int(y) and int(x) < x1 < self.left + self.width * self.cell_size - (int(x) - self.left)) or \
                        (x_or_y == 'x' and x1 == int(x) and int(y) < y1 < self.top + self.height * self.cell_size - (int(y) - self.top)):
                    self.board[i][f"{x1} {y1}"] = Road(self, (x1, y1))
                    # Спавн врагов с шансом ~ 15%
                    if random.randint(1, 7) == 1:
                        self.enemies.append(persons_and_camera.Enemy(self, (x1, y1)))

    def generation(self):
        # Пока не сгенерируеться без ошибки (шанс на ошибку примерно 1 к 40)
        while True:
            try:
                center = 4
                # Списки крайних n линий клеток с каждой стороны
                extreme_coords_ud = []
                extreme_coords_lr = []
                for i in range(self.height):
                    for j in range(self.width):
                        x = self.left + j * self.cell_size
                        y = self.top + i * self.cell_size
                        # Проверка подходит ли координаты, (крайние клетки, без углов)
                        if (0 < i < MASK) and (MASK < j < self.width - MASK) and \
                                (not f"{x + self.cell_size} {y}" in extreme_coords_ud and not f"{x - self.cell_size} {y}" in extreme_coords_ud and
                                 not f"{x + self.cell_size * 2} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 2} {y}" in extreme_coords_ud and
                                 not f"{x + self.cell_size * 3} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 3} {y}" in extreme_coords_ud):
                            extreme_coords_ud.append(f"{x} {y}")
                        # Проверка подходит ли координаты, (крайние клетки, без углов)
                        if (0 < j < MASK) and (MASK < i < self.height - MASK) and \
                                (not f"{x} {y + self.cell_size}" in extreme_coords_lr and not f"{x} {y - self.cell_size}" in extreme_coords_lr and
                                 not f"{x} {y + self.cell_size * 2}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 2}" in extreme_coords_lr and
                                 not f"{x} {y + self.cell_size * 3}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 3}" in extreme_coords_lr):
                            extreme_coords_lr.append(f"{x} {y}")
                # Спавн дорог -----------------------------------------
                # height
                for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
                    x, y = extreme_coords_lr.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
                    # Прокладывание дороги в матрице
                    self.add_roads(x, y, 'y')
                # width
                for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
                    x, y = extreme_coords_ud.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
                    # Прокладывание дороги в матрице
                    self.add_roads(x, y, 'x')
                # Нахождение клеток в которых можно спавнить площадь ратушу и дома -----------------------------------------
                coords_for_gen = []
                for i in range(self.height):
                    for j in range(self.width):
                        # Входит ли в диапозон
                        if (2 < i < self.height - 2) and (2 < j < self.width - 2):
                            # Координаты
                            x0, x1, x2 = self.left + (j - 1) * self.cell_size, self.left + j * self.cell_size, self.left + (j + 1) * self.cell_size
                            y0, y1, y2 = self.top + (i - 1) * self.cell_size, self.top + i * self.cell_size, self.top + (i + 1) * self.cell_size
                            # Пустые координаты
                            coords_empty = [(i - 1, f"{x0} {y0}", j), (i - 1, f"{x1} {y0}", j), (i - 1, f"{x2} {y0}", j),
                                            (i, f"{x0} {y1}", j), (i, f"{x1} {y1}", j), (i, f"{x2} {y1}", j),
                                            (i + 1, f"{x0} {y2}", j), (i + 1, f"{x1} {y2}", j), (i + 1, f"{x2} {y2}", j)]
                            # Проверка есть ли дороги на координатах
                            coords_road_bool = any([any([self.board[i - 2][f"{x1} {y0 - self.cell_size}"].__class__.__name__ == 'Road',
                                                         self.board[i + 2][f"{x1} {y2 + self.cell_size}"].__class__.__name__ == 'Road']),
                                                    any([self.board[i][f"{x0 - self.cell_size} {y1}"].__class__.__name__ == 'Road',
                                                         self.board[i][f"{x2 + self.cell_size} {y1}"].__class__.__name__ == 'Road'])])
                            # Заполнение клеток дорогами
                            if all(list(map(lambda x: self.board[x[0]][x[1]].__class__.__name__ == 'Grass', coords_empty))) and coords_road_bool:
                                coords_for_gen.append(coords_empty)
                # Спавн площади -----------------------------------------
                # Поиск места для площади
                coords_square = None
                while coords_square is None:
                    num = random.randrange(len(coords_for_gen))
                    test = coords_for_gen[num]
                    # Если координаты входят в диапозон, то берём их
                    if (RANGE_SQUARE < test[center][0] < self.height - RANGE_SQUARE) and (
                            RANGE_SQUARE < test[center][2] < self.width - RANGE_SQUARE):
                        coords_square = coords_for_gen.pop(num)
                # Заполнение клеток дорогами
                for coord in coords_square:
                    self.board[coord[0]][coord[1]] = Road(self, coord[1].split())
                    # Спавн врагов с шансом 75%
                    if random.randint(1, 4) != 1:
                        self.enemies.append(persons_and_camera.Enemy(self, coord[1].split()))
                # Спавн домов -----------------------------------------
                for coords in coords_for_gen:
                    for i, coord in enumerate(coords):
                        # Переменные
                        x, y = list(map(int, coord[1].split()))
                        count_road = 0
                        count_house = 0
                        # Вычисляем всё кроме центра
                        if i != 4:
                            if self.board[coord[0]][coord[1]].__class__.__name__ == 'Grass':
                                around_coords = [self.board[coord[0] - 1][f"{x - GAME_CELL_SIZE} {y - GAME_CELL_SIZE}"], self.board[coord[0]][f"{x - GAME_CELL_SIZE} {y}"],
                                                 self.board[coord[0] - 1][f"{x} {y - GAME_CELL_SIZE}"], self.board[coord[0] + 1][f"{x - GAME_CELL_SIZE} {y + GAME_CELL_SIZE}"],
                                                 self.board[coord[0] + 1][f"{x + GAME_CELL_SIZE} {y + GAME_CELL_SIZE}"], self.board[coord[0]][f"{x + GAME_CELL_SIZE} {y}"],
                                                 self.board[coord[0] + 1][f"{x} {y + GAME_CELL_SIZE}"], self.board[coord[0] - 1][f"{x + GAME_CELL_SIZE} {y - GAME_CELL_SIZE}"]]
                                for around_coord in around_coords:
                                    if around_coord.__class__.__name__ == 'Road':
                                        count_road += 1
                                    if around_coord.__class__.__name__ == 'House':
                                        count_house += 1
                                # Если впритык к дороге, то проверяем сколько домо вокруг, если 0, то ставим, если больше, то с шансом 25% будет дом
                                if count_road >= 2 and ((count_house == 0) or (random.randint(1, 4) == 1 and count_house >= 1)) and coord not in coords_square:
                                    self.board[coord[0]][coord[1]] = House(self, (x, y))
                # Спавн ратуши -----------------------------------------
                # Выбор с какой стороны от площади будет ратуша
                for _ in range(4):
                    x_or_y = random.choice(['x', 'y'])
                    num = random.choice([3, -3])
                    coords_txt = list(map(int, coords_square[center][1].split()))
                    # Проверка, что ратуша не перекрывает не одну из дорог
                    if ((x_or_y == 'y' and \
                            (self.board[coords_square[center][0] + num][f"{coords_txt[0]} {coords_txt[1] + GAME_CELL_SIZE * num}"].__class__.__name__ != 'Road' and
                             self.board[coords_square[center][0] + (num // 3 * 4)][f"{coords_txt[0]} {coords_txt[1] + GAME_CELL_SIZE * (num // 3 * 4)}"].__class__.__name__ != 'Road') or
                            (x_or_y == 'x' and
                              self.board[coords_square[center][0]][f"{coords_txt[0] + GAME_CELL_SIZE * num} {coords_txt[1]}"].__class__.__name__ != 'Road' and
                              self.board[coords_square[center][0]][f"{coords_txt[0] + GAME_CELL_SIZE * (num // 3 * 4)} {coords_txt[1]}"].__class__.__name__ != 'Road'))):
                        break
                # Заполнение клеток ратушой
                spawn_town_hall = True
                for coord in coords_square:
                    # Вычисление координат \/
                    coords_txt = list(map(int, coord[1].split()))
                    if x_or_y == 'x':
                        coord_i = coord[0]
                        coord_x = coords_txt[0] + GAME_CELL_SIZE * num
                        coord_y = coords_txt[1]
                    if x_or_y == 'y':
                        coord_i = coord[0] + num
                        coord_x = coords_txt[0]
                        coord_y = coords_txt[1] + GAME_CELL_SIZE * num
                    # Если мы впритык к площади ставим дорогу, иначе ставим ратушу
                    if (x_or_y == 'x' and num == 3 and coords_txt[0] == int(coords_square[0][1].split()[0])) or \
                            ((x_or_y == 'x' and num == -3 and coords_txt[0] == int(coords_square[2][1].split()[0])) or
                             (x_or_y == 'y' and num == 3 and coord[0] == coords_square[0][0]) or
                             (x_or_y == 'y' and num == -3 and coord[0] == coords_square[6][0])):
                        if self.board[coord_i][f"{coord_x} {coord_y}"] in self.houses_sprites:
                            self.houses_sprites.remove(self.board[coord_i][f"{coord_x} {coord_y}"])
                        self.board[coord_i][f"{coord_x} {coord_y}"] = Road(self, (coord_x, coord_y))
                    elif spawn_town_hall:
                        # Запоминание данных, для того что бы добавить ратушу потом
                        if x_or_y == 'x' and num == 3:
                            angle = 0
                        elif x_or_y == 'x' and num == -3:
                            angle = 1
                        elif x_or_y == 'y' and num == 3:
                            angle = 2
                        elif x_or_y == 'y' and num == -3:
                            angle = 3
                        data = [coord_i, coord_x, coord_y, angle]
                        spawn_town_hall = False
                # Удаление домов впритык к ратуше
                x, y = list(map(int, coords_square[center][1].split()))
                iy = coords_square[center][0]
                # Вычисление координат /\ \/
                if x_or_y == 'x':
                    x += GAME_CELL_SIZE * num
                if x_or_y == 'y':
                    iy += num
                    y += GAME_CELL_SIZE * num
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        # Заменяем на траву если тут стоит дом
                        if self.board[iy + i][f"{x + GAME_CELL_SIZE * j} {y + GAME_CELL_SIZE * i}"].__class__.__name__ == 'House':
                            self.board[iy + i][f"{x + GAME_CELL_SIZE * j} {y + GAME_CELL_SIZE * i}"].kill()
                            self.board[iy + i][f"{x + GAME_CELL_SIZE * j} {y + GAME_CELL_SIZE * i}"] = Grass(self, (
                            x + GAME_CELL_SIZE * j, y + GAME_CELL_SIZE * i))
                # Добавление ратуши, сейчас для того что бы перекрыть всё остальное
                self.board[data[0]][f"{data[1]} {data[2]}"] = TownHall(self, (data[1], data[2]), data[3])
                self.Town_Hall = self.board[data[0]][f"{data[1]} {data[2]}"]
                # Если всё сработало - выходим из цикла
                break
            except Exception as exc:
                # Если ошибка - попробовать ещё раз
                print('Ошибка')
                print(exc)

    def render(self, screen):
        # Отрисовка, визуализация матрицы
        self.all_sprites.draw(screen)
        self.enemies_sprites.draw(screen)
        self.sword_sprites.draw(screen)
        self.houses_sprites.draw(screen)
        self.townhall_sprites.draw(screen)
