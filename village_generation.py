import pygame
import random


N = 15
CELL_SIZE = 50

pygame.init()
size = width, height = N * CELL_SIZE, N * CELL_SIZE
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Деревня')


class Village:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 0
        self.top = 0
        self.cell_size = CELL_SIZE

        self.COLOR_HOUSE = (116, 73, 42)
        self.COLOR_ROAD = (164, 138, 106)
        self.COLOR_GRASS = (75, 126, 58)

        self.board = {}

        x = self.left
        y = self.top

        for i in range(height):
            for j in range(width):
                self.board[f"{x} {y}"] = None
                x += self.cell_size
            x = self.left
            y += self.cell_size
        self.generation()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.generation()

    def generation(self):
        pass

    def render(self, screen):
        x = self.left
        y = self.top
        for i in range(self.height):
            for j in range(self.width):
                if self.board[f"{x} {y}"] == 'house':
                    pygame.draw.rect(screen, self.COLOR_HOUSE, (x, y, self.cell_size, self.cell_size))
                elif self.board[f"{x} {y}"] == 'road':
                    pygame.draw.rect(screen, self.COLOR_ROAD, (x, y, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, self.COLOR_GRASS, (x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            x = self.left
            y += self.cell_size


village = Village(N, N)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    village.render(screen)
    pygame.display.flip()
