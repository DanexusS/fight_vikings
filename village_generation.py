import pygame
import random


# Константы
N = 20
CELL_SIZE = 40
MIN_ROAD = 2
MAX_ROAD = 4

pygame.init()
size = width, height = N * CELL_SIZE, N * CELL_SIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Деревня')


class Village:
    def __init__(self, width, height):
        # Переменные поля и клеток
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = CELL_SIZE
        # Цвета
        self.COLOR_HOUSE = (116, 73, 42)
        self.COLOR_ROAD = (164, 138, 106)
        self.COLOR_GRASS = (75, 126, 58)
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
        # Списки крайних трёх линий клеток с каждой стороны
        extreme_coords_ud = []
        extreme_coords_lr = []
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                if (0 < i < 4) and (4 < j < self.width - 5) and \
                        (not f"{x + self.cell_size} {y}" in extreme_coords_ud and not f"{x - self.cell_size} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 2} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 2} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 3} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 3} {y}" in extreme_coords_ud):
                    extreme_coords_ud.append(f"{x} {y}")
                if (0 < j < 4) and (4 < i < self.height - 5) and \
                        (not f"{x} {y + self.cell_size}" in extreme_coords_lr and not f"{x} {y - self.cell_size}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 2}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 2}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 3}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 3}" in extreme_coords_lr):
                    extreme_coords_lr.append(f"{x} {y}")
        # Спавн дорог
        for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
            try:
                x, y = extreme_coords_lr.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            except Exception:
                print(extreme_coords_lr)
            for i in range(self.height):
                for j in range(self.width):
                    x1 = self.left + j * self.cell_size
                    y1 = self.top + i * self.cell_size
                    if y1 == int(y) and int(x) < x1 < self.width * self.cell_size - int(x):
                        self.board[i][f"{x1} {y1}"] = 'road'
        for _ in range(random.randint(MIN_ROAD, MAX_ROAD)):
            try:
                x, y = extreme_coords_ud.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            except Exception:
                print(extreme_coords_ud)
            for i in range(self.height):
                for j in range(self.width):
                    x1 = self.left + j * self.cell_size
                    y1 = self.top + i * self.cell_size
                    if x1 == int(x) and int(y) < y1 < self.height * self.cell_size - int(y):
                        self.board[i][f"{x1} {y1}"] = 'road'
        # Генерация площади и домов
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
        while True:
            num = random.randrange(len(coords_for_gen))
            test = coords_for_gen[num]
            print(test)
            if (N // 2.5 < test[4][0] < self.height - N // 2.5) and (N // 2.5 < test[4][2] < self.width - N // 2.5):
                coords_square = coords_for_gen.pop(num)
                break
        for coord in coords_square:
            self.board[coord[0]][coord[1]] = 'road'
        for coords in coords_for_gen:
            count = 0
            for i, coord in enumerate(coords):
                if i == 4:
                    cell = coord
                elif self.board[coord[0]][coord[1]] != 'road':
                    count += 1
            if count == 8:
                self.board[cell[0]][cell[1]] = 'house'
        # далее ---


    def render(self, screen):
        # Отрисовка, визуализация матрицы
        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][f"{x} {y}"] == 'house':
                    pygame.draw.rect(screen, self.COLOR_HOUSE, (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
                elif self.board[i][f"{x} {y}"] == 'road':
                    pygame.draw.rect(screen, self.COLOR_ROAD, (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(screen, self.COLOR_GRASS, (x + 1, y + 1, self.cell_size - 1, self.cell_size - 1))
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
