import pygame
import random


# Константы
N = 15
CELL_SIZE = 50

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
        # Список крайних трёх линий клеток с каждой стороны
        extreme_coords = []
        for i in range(self.height):
            for j in range(self.width):
                x = self.left + j * self.cell_size
                y = self.top + i * self.cell_size
                if i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1 or \
                        (i == 1 or i == self.height - 2 or j == 1 or j == self.width - 2 or
                         i == 2 or i == self.height - 3 or j == 2 or j == self.width - 3):
                    extreme_coords.append(f"{x} {y}")
        pass

    def render(self, screen):
        # Отрисовка, визуализация матрицы
        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][f"{x} {y}"] == 'house':
                    pygame.draw.rect(screen, self.COLOR_HOUSE, (x, y, self.cell_size, self.cell_size))
                elif self.board[i][f"{x} {y}"] == 'road':
                    pygame.draw.rect(screen, self.COLOR_ROAD, (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, self.COLOR_GRASS, (x, y, self.cell_size, self.cell_size))
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
