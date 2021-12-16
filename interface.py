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
        self.offset = start_pos

        self.height = len(self.inventory.slots) // num_of_rows
        self.width = len(self.inventory.slots) // self.height
        self.mouse_slot = None

    def render_slots(self, scr):
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(scr, pygame.Color(SLOT),
                                 pygame.Rect((CELL_SIZE + self.space.x) * x + self.offset.x,
                                             (CELL_SIZE + self.space.y) * y + self.offset.y,
                                             CELL_SIZE, CELL_SIZE), 1)

    def covers_slots(self, cell: Vector2):
        return 0 <= cell.x <= self.width and 0 <= cell.y <= self.height

    def get_cell(self, mouse_pos) -> Vector2:
        x = int((mouse_pos[0] - self.offset.x) // CELL_SIZE)
        y = int((mouse_pos[1] - self.offset.y) // CELL_SIZE)

        return Vector2(x, y)

    def drop_item(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[cell.x + cell.y]
            if slot.item.ID != -1:
                self.inventory.swap_item(self.mouse_slot, slot)
                self.mouse_slot = None

    def slot_clicked(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[cell.x + cell.y]
            if slot.item.ID != -1:
                self.mouse_slot = slot

    def moving_item(self, mouse_pos):
        pass


interface = Interface(Inventory(60), Vector2(2.5, 2.5), Vector2(50, 62.5), 10)

size = w, h = 450, 450
screen = pygame.display.set_mode(size)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            interface.slot_clicked(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            interface.moving_item(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            interface.drop_item(event.pos)

    screen.fill(pygame.Color(BG))
    interface.render_slots(screen)
    pygame.display.flip()
