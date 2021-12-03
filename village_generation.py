import pygame
import random


# Константы
N = 30
CELL_SIZE = 20

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
        x = self.left
        y = self.top
        for i in range(self.height):
            self.board.append({})
            for j in range(self.width):
                self.board[i][f"{x} {y}"] = None
                x += self.cell_size
            x = self.left
            y += self.cell_size
        # Генерация
        self.generation()

    def set_view(self, left, top, cell_size):
        # Установка новых значений
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generation()

    def generation(self):
        # Списоки крайних трёх линий клеток с каждой стороны
        extreme_coords_ud = []
        extreme_coords_lr = []
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                if (0 < i < 3) and (j != 0 and j != 1 and j != 2 and j != self.width - 1 and j != self.width - 2 and j != self.width - 3) and \
                        (not f"{x + self.cell_size} {y}" in extreme_coords_ud and not f"{x - self.cell_size} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 2} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 2} {y}" in extreme_coords_ud and
                         not f"{x + self.cell_size * 3} {y}" in extreme_coords_ud and not f"{x - self.cell_size * 3} {y}" in extreme_coords_ud):
                    extreme_coords_ud.append(f"{x} {y}")
                if (0 < j < 3) and (i != 0 and i != 1 and i != 2 and i != self.height - 1 and i != self.height - 2 and i != self.height - 3) and \
                        (not f"{x} {y + self.cell_size}" in extreme_coords_lr and not f"{x} {y - self.cell_size}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 2}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 2}" in extreme_coords_lr and
                         not f"{x} {y + self.cell_size * 3}" in extreme_coords_lr and not f"{x} {y - self.cell_size * 3}" in extreme_coords_lr):
                    extreme_coords_lr.append(f"{x} {y}")
        # Спавн дорог
        for _ in range(random.randint(2, N // 5)):
            x, y = extreme_coords_lr.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            for i in range(self.height):
                for j in range(self.width):
                    x1 = self.left + j * self.cell_size
                    y1 = self.top + i * self.cell_size
                    if y1 == int(y) and int(x) < x1 < self.width * self.cell_size - int(x):
                        self.board[i][f"{x1} {y1}"] = 'road'
        for _ in range(random.randint(1, N // 5)):
            x, y = extreme_coords_ud.pop(random.randint(0, len(extreme_coords_lr) - 1)).split()
            for i in range(self.height):
                for j in range(self.width):
                    x1 = self.left + j * self.cell_size
                    y1 = self.top + i * self.cell_size
                    if x1 == int(x) and int(y) < y1 < self.height * self.cell_size - int(y):
                        self.board[i][f"{x1} {y1}"] = 'road'


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
