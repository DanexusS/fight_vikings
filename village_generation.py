import pygame
import os

from constants import *


def load_image(name):
    fullname = os.path.join('images/', name)
    image = pygame.image.load(fullname).convert_alpha()
    return image


class House(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.houses_sprites, other.all_sprites)
        # Переменные
        self.hp = 10
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('house.png'), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])

    def damage(self, dmg):
        if self.hp > 0:
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
            return self.status
        return None


class TownHall(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.townhall_sprites, other.all_sprites)
        # Переменные
        self.hp = 100
        self.status = 'normal'
        self.image = pygame.transform.scale(load_image('townhall.png'), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])

    def damage(self, dmg):
        if self.hp > 0:
            self.hp -= dmg
            if self.hp < 1:
                self.status = 'destroed'
                self.hp = 0
            return self.status
        return None


class Road(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.all_sprites)
        # Переменные
        self.image = pygame.transform.scale(load_image('road.png'), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


class Grass(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.all_sprites)
        # Переменные
        self.image = pygame.transform.scale(load_image('grass.png'), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


class Tree(pygame.sprite.Sprite):
    def __init__(self, other, pos):
        super().__init__(other.trees_sprites, other.all_sprites)
        # Переменные
        self.image = pygame.transform.scale(load_image('tree.png'), (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = int(pos[0])
        self.rect.y = int(pos[1])


# =======================================================================================================
class Village:
    def __init__(self, width, height):
        # Переменные поля и клеток
        self.width = width
        self.height = height
        self.cell_size = CELL_SIZE
        self.left = EMPTY_N * CELL_SIZE
        self.top = EMPTY_N * CELL_SIZE

        self.all_sprites = pygame.sprite.Group()
        self.houses_sprites = pygame.sprite.Group()
        self.townhall_sprites = pygame.sprite.Group()
        self.trees_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()

        self.houses = []
        self.townhalls = []
        # Пустые клетки вокруг деревни
        for i in range(-N, self.height + N * 2):
            for j in range(-N, self.width + N * 2):
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

    def set_view(self, left, top, cell_size=CELL_SIZE):
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

    def generation(self):
        # Пока не сгенерируеться без ошибки (шанс на ошибку примерно 1 к 50)
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
                    if (RANGE_SQUARE < test[center][0] < self.height - RANGE_SQUARE) and (RANGE_SQUARE < test[center][2] < self.width - RANGE_SQUARE):
                        coords_square = coords_for_gen.pop(num)
                # Заполнение клеток дорогами
                for coord in coords_square:
                    self.board[coord[0]][coord[1]] = Road(self, coord[1].split())
                # Спавн домов -----------------------------------------
                for coords in coords_for_gen:
                    count_not_road = 0
                    count_not_house = 0
                    for i, coord in enumerate(coords):
                        # Вычисляем центр квадрата координат (куда будем ставить дом), и сколько дорог вокруг
                        if i == 4:
                            cell = coord
                        else:
                            if self.board[coord[0]][coord[1]].__class__.__name__ != 'Road':
                                count_not_road += 1
                            if self.board[coord[0]][coord[1]].__class__.__name__ != 'House':
                                count_not_house += 1
                    # Если вокруг нет дорог то идём дальше
                    if count_not_road >= 8:
                        # Если вокруг нет домов то ставим дом, иначе с шансом 33% будет дом
                        if (count_not_house >= 8) or (count_not_house < 8 and random.randint(1, 3) == 1):
                            self.board[cell[0]][cell[1]] = House(self, cell[1].split())
                # Спавн ратуши -----------------------------------------
                # Выбор с какой стороны от площади будет ратуша
                for _ in range(4):
                    x_or_y = random.choice(['x', 'y'])
                    num = random.choice([3, -3])
                    coords_txt = list(map(int, coords_square[center][1].split()))
                    # Проверка, что ратуша не перекрывает не одну из дорог
                    if ((x_or_y == 'y' and \
                            (self.board[coords_square[center][0] + num][f"{coords_txt[0]} {coords_txt[1] + CELL_SIZE * num}"].__class__.__name__ != 'Road' and
                             self.board[coords_square[center][0] + (num // 3 * 4)][f"{coords_txt[0]} {coords_txt[1] + CELL_SIZE * (num // 3 * 4)}"].__class__.__name__ != 'Road') or
                            (x_or_y == 'x' and
                              self.board[coords_square[center][0]][f"{coords_txt[0] + CELL_SIZE * num} {coords_txt[1]}"].__class__.__name__ != 'Road' and
                              self.board[coords_square[center][0]][f"{coords_txt[0] + CELL_SIZE * (num // 3 * 4)} {coords_txt[1]}"].__class__.__name__ != 'Road'))):
                        break
                # Заполнение клеток ратуши
                for coord in coords_square:
                    # Вычисление координат \/
                    coords_txt = list(map(int, coord[1].split()))
                    if x_or_y == 'x':
                        coord_i = coord[0]
                        coord_x = coords_txt[0] + CELL_SIZE * num
                        coord_y = coords_txt[1]
                    if x_or_y == 'y':
                        coord_i = coord[0] + num
                        coord_x = coords_txt[0]
                        coord_y = coords_txt[1] + CELL_SIZE * num
                    # Если мы впритык к площади ставим дорогу, иначе ставим ратушу
                    if (x_or_y == 'x' and num == 3 and coords_txt[0] == int(coords_square[0][1].split()[0])) or \
                            ((x_or_y == 'x' and num == -3 and coords_txt[0] == int(coords_square[2][1].split()[0])) or
                             (x_or_y == 'y' and num == 3 and coord[0] == coords_square[0][0]) or
                             (x_or_y == 'y' and num == -3 and coord[0] == coords_square[6][0])):
                        self.board[coord_i][f"{coord_x} {coord_y}"] = Road(self, (coord_x, coord_y))
                    else:
                        self.board[coord_i][f"{coord_x} {coord_y}"] = TownHall(self, (coord_x, coord_y))
                # Удаление домов впритык к ратуше
                x, y = list(map(int, coords_square[center][1].split()))
                iy = coords_square[center][0]
                # Вычисление координат /\ \/
                if x_or_y == 'x':
                    x += CELL_SIZE * num
                if x_or_y == 'y':
                    iy += num
                    y += CELL_SIZE * num
                for i in range(-2, 3):
                    for j in range(-2, 3):
                        # Заменяем на траву если тут стоит дом
                        if self.board[iy + i][f"{x + CELL_SIZE * j} {y + CELL_SIZE * i}"].__class__.__name__ == 'House':
                            self.board[iy + i][f"{x + CELL_SIZE * j} {y + CELL_SIZE * i}"].kill()
                            self.board[iy + i][f"{x + CELL_SIZE * j} {y + CELL_SIZE * i}"] = Grass(self, (x + CELL_SIZE * j, y + CELL_SIZE * i))
                # Если всё сработало - выходим из цикла
                break
            except Exception:
                # Если ошибка - попробовать ещё раз
                print('Ошибка')
                pass

    def render(self, screen):
        # Отрисовка, визуализация матрицы
        self.all_sprites.draw(screen)
