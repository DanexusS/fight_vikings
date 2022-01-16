import pygame
import item_database

from inventory_obj import *
from pygame import Vector2
from player_inventory import *


# Инициализация дополнительных компонентов
pygame.init()
item_db = item_database.init()

# Константы
BG_COLOR = pygame.Color("#43485E")
SLOT_COLORS = {
    "Frame": pygame.Color("#C8D1F7"),
    "Hovered_BG": pygame.Color("#60667e"),
    "Info_BG": pygame.Color("#787d91"),
    "Amount_Text": pygame.Color("#d0d1d6"),
}
INV_SLOT_SIZE = 128
AMOUNT_FONT = pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 4.5))
INFO_FONTS = {
    "Title": pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 4.75)),
    "Description": pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 5))
}
RUS_ATTRIBUTES = {
    Attributes.Move_Speed: "скорость",
    Attributes.Attack_Speed: "скорость атаки",
    Attributes.Damage: "урон"
}


PlayerAttributes()


size = w, h = 1920, 1080
screen = pygame.display.set_mode(size)


class Mouse:
    def __init__(self):
        self.clicked_slot = None
        self.hovered_slot = None
        self.position = Vector2()


class Interface:
    def __init__(self, inventory: Inventory, space: Vector2, start_pos: Vector2):
        self.inventory = inventory
        self.space = space
        self.offset = start_pos

        self.height = len(self.inventory.slots)
        self.width = len(self.inventory.slots[0])
        self.mouse = Mouse()

    def render_slots(self):
        for y in range(self.height):
            for x in range(self.width):
                cell_position = Vector2((INV_SLOT_SIZE + self.space.x) * x + self.offset.x,
                                        (INV_SLOT_SIZE + self.space.y) * y + self.offset.y)
                cell = pygame.Rect(cell_position.x, cell_position.y, INV_SLOT_SIZE, INV_SLOT_SIZE)
                slot = self.inventory.slots[y][x]

                """Отрисовка элементов слота и связанных с ним элементов"""
                # Отрисовка элементов при перекрытии слота курсором
                if slot.mouse_hovered:
                    # Отрисовка фона
                    pygame.draw.rect(screen, SLOT_COLORS["Hovered_BG"], cell, 0)

                # Отрисовка самого слота
                pygame.draw.rect(screen, SLOT_COLORS["Frame"], cell, 1)

                # Отрисовка информации о предмете в слоте
                self.draw_item_info(slot, cell_position)

        # Перемещение изображения предмета во временя перетаскивания
        if self.mouse.clicked_slot is not None and self.mouse.clicked_slot.is_moving:
            image = pygame.image.load(self.mouse.clicked_slot.ui_display)
            slot_image = pygame.transform.scale(image.convert_alpha(), (96, 96))
            rect = slot_image.get_rect(center=self.mouse.position)
            screen.blit(slot_image, rect)
        elif self.mouse.hovered_slot is not None and self.mouse.hovered_slot.item.ID != -1:
            item = self.mouse.hovered_slot.item
            title = INFO_FONTS["Title"].render(item.title, True, SLOT_COLORS["Amount_Text"], SLOT_COLORS["Info_BG"])

            screen.blit(title, (self.mouse.position.x + 15, self.mouse.position.y + 15))

            extra_info = []
            if item.TYPE == ItemType.Weapon or item.TYPE == ItemType.Equipment:
                if item.buffs is not None:
                    for buff in item.buffs:
                        extra_info.append(f"Характеристика '{RUS_ATTRIBUTES[buff.affected_attribute]}' увеличится "
                                          f"на {buff.value}")
            if item.TYPE == ItemType.Weapon:
                extra_info.append(f"Урон увеличивается на {item.damage.value}")

            y = 0
            for info in extra_info:
                info_text = INFO_FONTS["Description"].render(info, True, SLOT_COLORS["Amount_Text"],
                                                             SLOT_COLORS["Info_BG"])
                screen.blit(info_text, (self.mouse.position.x + 30,
                                        self.mouse.position.y + 30 * y + 48.5))
                y += 1

    #
    @staticmethod
    def draw_item_info(slot, cell_position):
        # Отрисовка изображения предмета в слоте
        if not slot.is_moving:
            if slot.ui_display is not None:
                slot_image = pygame.transform.scale(pygame.image.load(slot.ui_display).convert_alpha(),
                                                    (96, 96))
                rect = slot_image.get_rect(center=(cell_position.x + INV_SLOT_SIZE // 2,
                                                   cell_position.y + INV_SLOT_SIZE // 2))
                screen.blit(slot_image, rect)

            # Отрисовка кол-ва предметов в слоте
            screen.blit(AMOUNT_FONT.render(str(slot.amount) if slot.amount != 0 and slot.item.is_stackable else "",
                                           True, SLOT_COLORS["Amount_Text"]),
                        (cell_position.x + INV_SLOT_SIZE // 1.5, cell_position.y + INV_SLOT_SIZE // 1.5))

    #
    # Проверка, находится ли клетка в существующем слоте
    def covers_slots(self, cell: Vector2) -> bool:
        return 0 <= cell.x <= self.width and 0 <= cell.y <= self.height and \
               cell.x < self.width and cell.y < self.height

    #
    # Получение клетки из позиции мыши
    def get_cell(self, mouse_pos) -> Vector2:
        x = (mouse_pos[0] - self.offset.x) // (INV_SLOT_SIZE + self.space.x)
        y = (mouse_pos[1] - self.offset.y) // (INV_SLOT_SIZE + self.space.y)

        return Vector2(x, y)

    #
    # Вызывается при завершении перетаскивания предмета
    def drop_item(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell) and self.mouse.clicked_slot is not None:
            slot = self.inventory.slots[int(cell.y)][int(cell.x)]
            if self.mouse.clicked_slot.item.ID != -1:
                self.inventory.swap_item(self.mouse.clicked_slot, slot)
                self.mouse.clicked_slot.is_moving = False
                self.mouse.clicked_slot = None

    #
    # Вызывается при нажатии на слот
    def slot_clicked(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y)][int(cell.x)]
            if slot.item.ID != -1:
                self.mouse.clicked_slot = slot

    #
    # Проверка на перекрытие курсором слота
    def slot_hover(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        mouse_slot = self.mouse.hovered_slot

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y)][int(cell.x)]
            slot.mouse_hovered = True

            if mouse_slot is not None:
                self.mouse.hovered_slot.mouse_hovered = mouse_slot == slot

            self.mouse.hovered_slot = slot
        elif mouse_slot is not None:
            self.mouse.hovered_slot.mouse_hovered = False
            self.mouse.hovered_slot = None

    #
    # Вызывается при перемещении курсора
    def moving_item(self, mouse_pos):
        if self.mouse.clicked_slot is not None:
            self.mouse.clicked_slot.is_moving = True
        self.mouse.position = Vector2(mouse_pos[0], mouse_pos[1])


interface = Interface(Inventory(60, 10), Vector2(5, 5), Vector2(50, 62.5))
interface.inventory.add_item(item_db["Sword"])
interface.inventory.add_item(item_db["Stick"], 2)
interface.inventory.add_item(item_db["Helmet"])

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