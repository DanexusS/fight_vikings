"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


from inventory_obj import *
from constants import *


pygame.init()

# Константы текста
AMOUNT_FONT = pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 4.5))
INFO_FONTS = {
    "Title": pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 4.75)),
    "Description": pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 5))
}


class InterfaceTypes(Enum):
    Regular = 0,
    Equipment = 1


class Interface:
    def __init__(self, inventory: Inventory, space: Vector2, start_pos: Vector2, interface_type, allowed_types=None):
        self.inventory = inventory
        self.space = space
        self.offset = start_pos

        self.height = len(self.inventory.slots)
        self.width = len(self.inventory.slots[0])

        if allowed_types:
            if self.height == 1 and self.width == len(allowed_types):
                for i in range(self.width):
                    self.inventory.slots[0][i].allowed_types = [allowed_types[i]]

        self.opened = False
        self.TYPE = interface_type

    def render_slots(self, screen):
        types_row = ["sword", "helmet", "armor", "pants", "boots"] if self.height == 1 else []

        for y in range(self.height):
            for x in range(self.width):
                cell_position = Vector2((INV_SLOT_SIZE + self.space.x) * x + self.offset.x,
                                        (INV_SLOT_SIZE + self.space.y) * y + self.offset.y)
                cell = pygame.Rect(cell_position.x, cell_position.y, INV_SLOT_SIZE, INV_SLOT_SIZE)
                slot = self.inventory.slots[y][x]

                # Отрисовка элементов слота и связанных с ним элементов
                # # Отрисовка фона
                if slot.mouse_hovered:
                    pygame.draw.rect(screen, SLOT_COLORS["Hovered_BG"], cell, 0)
                # # Отрисовка изображения для слотов с ограничениями по типам
                if slot.item.ID == -1 and slot.allowed_types:
                    slot_image = pygame.transform.scale(pygame.image.load(f"images/ui_{types_row[x]}.png").convert_alpha(),
                                                        (96, 96))
                    rect = slot_image.get_rect(center=(cell_position.x + INV_SLOT_SIZE // 2,
                                                       cell_position.y + INV_SLOT_SIZE // 2))
                    screen.blit(slot_image, rect)

                # Отрисовка самого слота
                pygame.draw.rect(screen, SLOT_COLORS["Frame"], cell, 1)

                # Отрисовка информации о предмете в слоте
                self.draw_item_info(slot, cell_position, screen)

        # Вывод информации о предмете при наведении на него мышкой
        if not MOUSE.start_drag_slot and MOUSE.slot_hovered_over and MOUSE.slot_hovered_over.item.ID != -1:
            item = MOUSE.slot_hovered_over.item
            title = INFO_FONTS["Title"].render(item.title, True, SLOT_COLORS["Amount_Text"], SLOT_COLORS["Info_BG"])

            screen.blit(title, (MOUSE.position.x + 15, MOUSE.position.y + 15))

            extra_info = []
            if item.TYPE == ItemType.Weapon or item.TYPE == ItemType.Equipment:
                if item.buffs is not None:
                    for buff in item.buffs:
                        extra_info.append(f"""Характеристика "{RUS_ATTRIBUTES[buff.affected_attribute]}" увеличится """
                                          f"""на {buff.value}""")
            if item.TYPE == ItemType.Weapon:
                extra_info.append(f"Урон увеличивается на {item.damage.value}")

            for i in range(len(extra_info)):
                info_text = INFO_FONTS["Description"].render(extra_info[i], True, SLOT_COLORS["Amount_Text"],
                                                             SLOT_COLORS["Info_BG"])
                screen.blit(info_text, (MOUSE.position.x + 30,
                                        MOUSE.position.y + 30 * i + 48.5))

    #
    @staticmethod
    def draw_item_info(slot, cell_position, screen):
        if slot != MOUSE.start_drag_slot:
            # Отрисовка изображения предмета в слоте
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
        mouse_interface = MOUSE.current_interface
        cell = self.get_cell(mouse_pos)

        if mouse_interface is not None:
            if self.covers_slots(cell) and MOUSE.start_drag_slot is not None:
                slot = self.inventory.slots[int(cell.y)][int(cell.x)]
                if MOUSE.start_drag_slot.item.ID != -1:
                    self.inventory.swap_item(slot, MOUSE.start_drag_slot)
                    
                    MOUSE.start_drag_slot.is_moving = False
                    MOUSE.start_drag_slot = None

    #
    # Вызывается при нажатии на слот
    def slot_clicked(self, mouse_pos):
        cell = self.get_cell(mouse_pos)

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y)][int(cell.x)]
            if slot.item.ID != -1:
                MOUSE.start_drag_slot = slot

    #
    # Проверка, перекрывает ли мышка этот интерфейс
    def interface_check(self):
        cell = self.get_cell(MOUSE.position)

        if self.covers_slots(cell):
            MOUSE.current_interface = self

    #
    # Проверка на перекрытие курсором слота
    def mouse_move(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        mouse_slot = MOUSE.slot_hovered_over

        if self.covers_slots(cell):
            slot = self.inventory.slots[int(cell.y)][int(cell.x)]
            slot.mouse_hovered = True

            if mouse_slot:
                MOUSE.slot_hovered_over.mouse_hovered = mouse_slot == slot

            MOUSE.slot_hovered_over = slot
        elif mouse_slot:
            MOUSE.slot_hovered_over.mouse_hovered = False
            MOUSE.slot_hovered_over = None
            if not MOUSE.start_drag_slot:
                MOUSE.current_interface = None
