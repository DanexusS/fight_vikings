import pygame
from inventory_obj import *
from game_math import *


BG = "#43485E"
SLOT = "#C8D1F7"
CELL_SIZE = 32


class Interface:
    def __init__(self, inventory: Inventory, space: Vector2, start_pos: Vector2, num_of_rows: int):
        self.inventory = inventory
        self.space = space
        self.start_pos = start_pos
        self.height = len(self.inventory.slots) // num_of_rows
        self.width = len(self.inventory.slots) // self.height

    def render_slots(self, scr):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(scr, pygame.Color(SLOT),
                                 pygame.Rect((CELL_SIZE + self.space.x) * x + self.start_pos.x,
                                             (CELL_SIZE + self.space.y) * y + self.start_pos.y,
                                             CELL_SIZE, CELL_SIZE), 1, )


interface = Interface(Inventory(60), Vector2(2.5, 2.5), Vector2(50, 62.5), 10)

size = w, h = 450, 450
screen = pygame.display.set_mode(size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     board.get_click(event.pos)

    screen.fill(pygame.Color(BG))
    interface.render_slots(screen)
    pygame.display.flip()
