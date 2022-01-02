import pygame

from inventory_obj import *
from pygame import Vector2
from item_database_editor import init


pygame.init()
item_db = init()

BG_COLOR = pygame.Color("#43485E")
SLOT_COLORS = {
    "Frame": pygame.Color("#C8D1F7"),
    "BG": pygame.Color("#60667e"),
    "Amount_Text": pygame.Color("#d0d1d6")
}
CELL_SIZE = 128
AMOUNT_FONT = pygame.font.SysFont("Impact", round(CELL_SIZE // 4.5))


size = w, h = 1920, 1080
screen = pygame.display.set_mode(size)


class MouseData:
    def __init__(self):
        self.clicked_slot = None
        self.hovered_slot = None


class Interface:
    def __init__(self, inventory: Inventory, space: Vector2, start_pos: Vector2):
        self.inventory = inventory
        self.space = space
        self.offset = start_pos

        self.height = len(self.inventory.slots)
        self.width = len(self.inventory.slots[0])
        self.mouse_data = MouseData()

    def render_slots(self):
        for y in range(self.height):
            for x in range(self.width):
                cell_position = ((CELL_SIZE + self.space.x) * x + self.offset.x,
                                 (CELL_SIZE + self.space.y) * y + self.offset.y)
                cell = pygame.Rect(cell_position[0], cell_position[1], CELL_SIZE, CELL_SIZE)
                slot = self.inventory.slots[y - 1][x - 1]

                if slot.mouse_hovered:
                    pygame.draw.rect(screen, SLOT_COLORS["BG"], cell, 0)
                pygame.draw.rect(screen, SLOT_COLORS["Frame"], cell, 1)

                if slot.ui_display is not None:
                    slot_image = pygame.transform.scale(pygame.image.load(slot.ui_display).convert_alpha(),
                                                        (96, 96))
                    rect = slot_image.get_rect(center=(cell_position[0] + CELL_SIZE // 2,
                                                       cell_position[1] + CELL_SIZE // 2))
                    screen.blit(slot_image, rect)

                screen.blit(
                    AMOUNT_FONT.render(str(slot.amount) if slot.amount != 0 else "",
                                       False,
                                       SLOT_COLORS["Amount_Text"]),
                    (cell_position[0] + CELL_SIZE // 1.5, cell_position[1] + CELL_SIZE // 1.5)
                )

    def covers_slots(self, cell: Vector2) -> bool:
        return 0 <= cell.x <= self.width and 0 <= cell.y <= self.height and \
               cell.x < self.width and cell.y < self.height

    def get_cell(self, mouse_pos) -> Vector2:
        x = (mouse_pos[0] - self.offset.x) // (CELL_SIZE + self.space.x)
        y = (mouse_pos[1] - self.offset.y) // (CELL_SIZE + self.space.y)

        return Vector2(x, y)

    def drop_item(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y) - 1][int(cell.x) - 1]
            if slot.item.ID != -1:
                self.inventory.swap_item(self.mouse_data.clicked_slot, slot)
                self.mouse_data.clicked_slot = None

    def slot_clicked(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y) - 1][int(cell.x) - 1]
            if slot.item.ID != -1:
                self.mouse_data.clicked_slot = slot

    def slot_hover(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        mouse_slot = self.mouse_data.hovered_slot

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y) - 1][int(cell.x) - 1]
            slot.mouse_hovered = True

            if mouse_slot is not None:
                self.mouse_data.hovered_slot.mouse_hovered = mouse_slot == slot

            self.mouse_data.hovered_slot = slot
        elif mouse_slot is not None:
            self.mouse_data.hovered_slot.mouse_hovered = False
            self.mouse_data.hovered_slot = None

    def moving_item(self, mouse_pos):
        pass


interface = Interface(Inventory(60, 10), Vector2(5, 5), Vector2(50, 62.5))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            interface.slot_clicked(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            interface.slot_hover(event.pos)
            interface.moving_item(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            interface.drop_item(event.pos)

    screen.fill(BG_COLOR)
    interface.render_slots()
    pygame.display.flip()
