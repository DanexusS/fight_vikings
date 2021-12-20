import pygame
import random


# Константы
N = random.randrange(20, 30, 2)
CELL_SIZE = 30

MIN_ROAD = N // 10
MAX_ROAD = MIN_ROAD * 2
MASK = N // 5
RANGE_SQUARE = N // 2.5

COLOR_HOUSE = (116, 73, 42)
COLOR_ROAD = (164, 138, 106)
COLOR_GRASS = (75, 126, 58)
COLOR_TOWN = (0, 156, 108)

pygame.init()
size = width, height = N * CELL_SIZE, N * CELL_SIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Деревня')


def add_roads(other, x, y, x_or_y):
    for i in range(other.height):
        for j in range(other.width):
            x1 = other.left + j * other.cell_size
            y1 = other.top + i * other.cell_size
            if (x_or_y == 'y' and y1 == int(y) and int(x) < x1 < other.width * other.cell_size - int(x)) or \
                    (x_or_y == 'x' and x1 == int(x) and int(y) < y1 < other.height * other.cell_size - int(y)):
                other.board[i][f"{x1} {y1}"] = 'road'


class Village:
    def __init__(self, width, height):
        # Переменные поля и клеток
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = CELL_SIZE
        # Матрица
        self.board = []
        for i in range(self.height):
            self.board.append({})
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                self.board[i][f"{x} {y}"] = None
        # Генерация
        self.generation()

    def set_view(self, left, top, cell_size):
        # Установка новых значений
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generation()

    def generation(self):
        center = 4
        # Списки крайних n линий клеток с каждой стороны
        extreme_coords_ud = []
        extreme_coords_lr = []
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                if (0 < i < MASK) and (MASK < j < self.width - MASK) and \
                        (not f"{x + self.cell_size} {y}" in extreme_coords_ud and not f"{x - self.cell_size} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 2} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 2} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 3} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 3} {y}" in extreme_coords_ud):
                    extreme_coords_ud.append(f"{x} {y}")
                if (0 < j < MASK) and (MASK < i < self.height - MASK) and \
                        (not f"{x} {y + self.cell_size}" in extreme_coords_lr and not f"{x} {y - self.cell_size}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 2}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 2}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 3}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 3}" in extreme_coords_lr):
                    extreme_coords_lr.append(f"{x} {y}")
        # Спавн дорог -----------------------------------------
        # H
        for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
            # Возможны ошибки, хотя возможно и нет
            try:
                x, y = extreme_coords_lr.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            except Exception:
                print(extreme_coords_lr)
            # Прокладывание дороги в матрице
            add_roads(self, x, y, 'y')
        # W
        for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
            # Возможны ошибки, хотя возможно и нет
            try:
                x, y = extreme_coords_ud.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            except Exception:
                print(extreme_coords_ud)
            # Прокладывание дороги в матрице
            add_roads(self, x, y, 'x')
        # Нахождение клеток в которых можно спавнить площадь ратушу и дома -----------------------------------------
        coords_for_gen = []
        for i in range(self.height):
            for j in range(self.width):
                if (2 < i < self.height - 2) and (2 < j < self.width - 2):
                    # Координаты
                    x0, x1, x2 = self.top + (j - 1) * self.cell_size, self.top + j * self.cell_size, self.top + (j + 1) * self.cell_size
                    y0, y1, y2 = self.top + (i - 1) * self.cell_size, self.top + i * self.cell_size, self.top + (i + 1) * self.cell_size
                    coords_empty = [(i - 1, f"{x0} {y0}", j), (i - 1, f"{x1} {y0}", j), (i - 1, f"{x2} {y0}", j),
                                    (i, f"{x0} {y1}", j), (i, f"{x1} {y1}", j), (i, f"{x2} {y1}", j),
                                    (i + 1, f"{x0} {y2}", j), (i + 1, f"{x1} {y2}", j), (i + 1, f"{x2} {y2}", j)]
                    coords_road_bool = any([any([self.board[i - 2][f"{x1} {y0 - self.cell_size}"] == 'road', self.board[i + 2][f"{x1} {y2 + self.cell_size}"] == 'road']),
                                       any([self.board[i][f"{x0 - self.cell_size} {y1}"] == 'road', self.board[i][f"{x2 + self.cell_size} {y1}"] == 'road'])])
                    # Заполнение клеток дорогами
                    if all(list(map(lambda x: not bool(self.board[x[0]][x[1]]), coords_empty))) and coords_road_bool:
                        coords_for_gen.append(coords_empty)
        # Спавн площади -----------------------------------------
        # Поиск места для площади
        coords_square = None
        while coords_square is None:
            num = random.randrange(len(coords_for_gen))
            test = coords_for_gen[num]
            if (RANGE_SQUARE < test[center][0] < self.height - RANGE_SQUARE) and (RANGE_SQUARE < test[center][2] < self.width - RANGE_SQUARE):
                coords_square = coords_for_gen.pop(num)
        # Заполнение клеток дорогами
        for coord in coords_square:
            self.board[coord[0]][coord[1]] = 'road'
        # Спавн домов -----------------------------------------
        for coords in coords_for_gen:
            count = 0
            for i, coord in enumerate(coords):
                if i == 4:
                    cell = coord
                elif self.board[coord[0]][coord[1]] != 'road':
                    count += 1
            if count == 8 and random.randint(1, 4) != 1:
                self.board[cell[0]][cell[1]] = 'house'
        # Спавн ратуши -----------------------------------------
        # Выбор с какой стороны от площади будет ратуша
        for _ in range(4):
            x_or_y = random.choice(['x', 'y'])
            num = random.choice([3, -3])
            coords_txt = list(map(int, coords_square[center][1].split()))
            # Проверка что ратуша не перекрывает не одну из дорог
            if ((x_or_y == 'y' and \
                    (self.board[coords_square[center][0] + num][f"{coords_txt[0]} {coords_txt[1] + CELL_SIZE * num}"] != 'road' and
                     self.board[coords_square[center][0] + (num // 3 * 4)][f"{coords_txt[0]} {coords_txt[1] + CELL_SIZE * (num // 3 * 4)}"] != 'road') or
                     (x_or_y == 'x' and
                      self.board[coords_square[center][0]][f"{coords_txt[0] + CELL_SIZE * num} {coords_txt[1]}"] != 'road' and
                      self.board[coords_square[center][0]][f"{coords_txt[0] + CELL_SIZE * (num // 3 * 4)} {coords_txt[1]}"] != 'road'))):
                break
        # Заполнение клеток ратуши
        for coord in coords_square:
            coords_txt = list(map(int, coord[1].split()))
            if x_or_y == 'x':
                coord_i = coord[0]
                coord_x = coords_txt[0] + CELL_SIZE * num
                coord_y = coords_txt[1]
            if x_or_y == 'y':
                coord_i = coord[0] + num
                coord_x = coords_txt[0]
                coord_y = coords_txt[1] + CELL_SIZE * num
            if (x_or_y == 'x' and num == 3 and coords_txt[0] == int(coords_square[0][1].split()[0])) or \
                    ((x_or_y == 'x' and num == -3 and coords_txt[0] == int(coords_square[2][1].split()[0])) or
                     (x_or_y == 'y' and num == 3 and coord[0] == coords_square[0][0]) or
                     (x_or_y == 'y' and num == -3 and coord[0] == coords_square[6][0])):
                self.board[coord_i][f"{coord_x} {coord_y}"] = 'road'
            else:
                self.board[coord_i][f"{coord_x} {coord_y}"] = 'town'
        # Удаление домов впритык к ратуше
        x, y = list(map(int, coords_square[center][1].split()))
        iy = coords_square[center][0]
        if x_or_y == 'x':
            x += CELL_SIZE * num
        if x_or_y == 'y':
            iy += num
            y += CELL_SIZE * num
        for i in range(-2, 3):
            for j in range(-2, 3):
                if self.board[iy + i][f"{x + CELL_SIZE * j} {y + CELL_SIZE * i}"] == 'house':
                    self.board[iy + i][f"{x + CELL_SIZE * j} {y + CELL_SIZE * i}"] = 'grass'
        # ---


    def render(self, screen):
        # Отрисовка, визуализация матрицы
        x = self.left
        y = self.top
        for i in range(self.height):
            for _ in range(self.width):
                coords = (x, y, self.cell_size, self.cell_size)
                if self.board[i][f"{x} {y}"] == 'house':
                    pygame.draw.rect(screen, COLOR_HOUSE, coords)
                elif self.board[i][f"{x} {y}"] == 'road':
                    pygame.draw.rect(screen, COLOR_ROAD, coords)
                elif self.board[i][f"{x} {y}"] == 'town':
                    pygame.draw.rect(screen, COLOR_TOWN, coords)
                else:
                    pygame.draw.rect(screen, COLOR_GRASS, coords)
                x += self.cell_size
            x = self.left
            y += self.cell_size

# Создание поля
village = Village(N, N)
# основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    village.render(screen)
    pygame.display.flip()
