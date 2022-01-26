"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""

import sys
import threading

from player_class import *
from interface import *
from general_stuff import *
from village import Village

# Создание окна pygame
pygame.init()

size = width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption('Fight Vikings')

# Нужные константы для игры
FONT_BTN = pygame.font.SysFont('Arial', 50)
FONT_LOAD = pygame.font.SysFont('Impact', 60)

# Позиции кнопок в меню
pos_exit = (width // 2 - SIZE_MENU_BTN.x // 2, height // 2 + 300 - SIZE_MENU_BTN.y // 2)
pos_play = (pos_exit[0], pos_exit[1] - 100)

# Фон
screen.fill(BG)

ATTRIBUTE_FONT = pygame.font.SysFont("Impact", round(INV_SLOT_SIZE / 4))


# Игра
class MainGame:
    def __init__(self):
        self.player = None
        self.village = None
        self.camera = None
        self.player_interfaces = None

    @staticmethod
    def draw_menu():
        # Кнопка выход
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_exit[0] - 4, pos_exit[1] + 4, SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        pygame.draw.rect(screen, BG_BTN, (pos_exit[0], pos_exit[1], SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        screen.blit(FONT_BTN.render('Выход', True, (0, 0, 0)), (pos_exit[0] + 85, pos_exit[1] + 10))

        # Кнопка начать игру
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_play[0] - 4, pos_play[1] + 4, SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        pygame.draw.rect(screen, BG_BTN, (pos_play[0], pos_play[1], SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        screen.blit(FONT_BTN.render('Играть', True, (0, 0, 0)), (pos_play[0] + 85, pos_play[1] + 10))

        # Обновить
        pygame.display.flip()

    @staticmethod
    def draw_load():
        # Надпись загрузки
        screen.fill(BG)
        screen.blit(FONT_LOAD.render('Загрузка...', True, BG_BTN), (width // 2 - 120, height // 2))

        # Обновить
        pygame.display.flip()

    @staticmethod
    def draw_died():
        surf = load_image('bg_die.png')
        rect = surf.get_rect()
        screen.blit(surf, rect)

        # Кнопка выход
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_exit[0] - 4, pos_exit[1] + 4, SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        pygame.draw.rect(screen, BG_BTN, (pos_exit[0], pos_exit[1], SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        screen.blit(FONT_BTN.render('Выход', True, (0, 0, 0)), (pos_exit[0] + 85, pos_exit[1] + 10))

    def inventory_opened(self):
        thread = threading.Thread(target=self.player_interfaces[0].render_slots(screen))
        thread.daemon = True
        thread.start()

        running_inv = True
        while running_inv:
            # Основные события, нужные для работы инвенторя
            for event in pygame.event.get():
                if MOUSE.current_interface:
                    if event.type == pygame.QUIT:
                        running_inv = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        MOUSE.current_interface.slot_clicked(event.pos)
                    if event.type == pygame.MOUSEMOTION:
                        MOUSE.current_interface.mouse_move(event.pos)
                    if event.type == pygame.MOUSEBUTTONUP:
                        MOUSE.current_interface.drop_item(event.pos)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                        if MOUSE.slot_hovered_over:
                            MOUSE.slot_hovered_over.mouse_hovered = False
                            MOUSE.slot_hovered_over = None
                        self.on_inventory_close(self.player_interfaces)

            MOUSE.position = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            screen.fill(BG_COLOR)
            # Отрисовка слотов у инвентарей и проверка на перекрытие их мышкой
            for interface in self.player_interfaces:
                interface.interface_check()
                interface.render_slots(screen)

            # Отображение всех характеристик героя
            y = 0
            for key, value in self.player.attributes.items():
                text = ATTRIBUTE_FONT.render(f"{RUS_ATTRIBUTES[key].capitalize()} -> {value.current_value}",
                                             True, BG_BTN)
                screen.blit(text, (1425, y * 35 + 52.5))
                y += 1

            # Перемещение изображения предмета во время перетаскивания
            if MOUSE.start_drag_slot:
                image = pygame.image.load(MOUSE.start_drag_slot.ui_display)
                slot_image = pygame.transform.scale(image.convert_alpha(), (96, 96))
                rect = slot_image.get_rect(center=MOUSE.position)
                screen.blit(slot_image, rect)
            pygame.display.flip()

    def on_inventory_close(self, interfaces):
        i = 0
        for interface in interfaces:
            interface.save(i)
            i += 1
        self.main_game()

    def on_inventory_open(self):
        fieldnames = ["item", "amount"]

        for i in range(len(self.player_interfaces)):
            file = open(f"inventory_{i}.csv", newline="")
            reader = list(DictReader(file, fieldnames, delimiter=";", quoting=QUOTE_NONNUMERIC))[1:]
            row_count = len(self.player_interfaces[i].inventory.slots)
            row = 0
            column = 0
            for line in reader:
                if row >= row_count:
                    row = 0
                    column += 1

                slot = InventorySlot(ITEMS_DB[line["title"]], int(line["amount"]))
                self.player_interfaces[i].inventory.set_slot(row, column, slot)

                row += 1

        self.inventory_opened()

    def main_game(self):
        screen.fill(BG)

        running_game = True
        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(BG)
                        self.draw_main_menu()
                    if event.key == pygame.K_i and self.player.state != PlayerStates.Dead:
                        screen.fill(BG_COLOR)
                        self.on_inventory_open()
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if self.player.state == PlayerStates.Dead and \
                            pos_exit[0] <= mouse_pos.x <= pos_exit[0] + SIZE_MENU_BTN.x and \
                            pos_exit[1] <= mouse_pos.y <= pos_exit[1] + SIZE_MENU_BTN.y:
                        screen.fill(BG)
                        self.draw_main_menu()

                self.player.update(event)

            MOUSE.position = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            # Ходьба героя
            for direction in self.player.directions.items():
                self.player.move_player(direction, self.village)

            # Атака героя
            self.player.attack(self.village)

            # Обновления врагов
            for enemy in self.village.enemies_sprites:
                enemy.update(self.village)

            # Обновление камеры
            self.camera.update(self.player, width, height)
            for sprite in self.village.all_sprites:
                self.camera.apply(sprite)

            # Отображение всей деревни
            self.village.render(screen)

            # Отображение экрана смерти, если игрок умер
            if self.player.state == PlayerStates.Dead:
                self.draw_died()

            # Обновление экрана
            pygame.display.flip()
            pygame.time.delay(10)

    @staticmethod
    def button_hover(mouse_pos: Vector2):
        if pos_exit[0] <= mouse_pos.x <= pos_exit[0] + SIZE_MENU_BTN.x and \
                pos_exit[1] <= mouse_pos.y <= pos_exit[1] + SIZE_MENU_BTN.y:
            return "Exit"
        if pos_play[0] <= mouse_pos.x <= pos_play[0] + SIZE_MENU_BTN.x and \
                pos_play[1] <= mouse_pos.y <= pos_play[1] + SIZE_MENU_BTN.y:
            return "Play"

        return None

    def draw_main_menu(self):
        # Создание объектов
        thread = threading.Thread(target=self.draw_menu)
        thread.daemon = True
        thread.start()

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    MOUSE.position = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    button = self.button_hover(MOUSE.position)

                    if button == "Exit":
                        sys.exit()
                    if button == "Play":
                        thread = threading.Thread(target=self.draw_load)
                        thread.daemon = True
                        thread.start()
                        main_village = Village()
                        main_village.load('save.csv')
                        main_village.start()

            #             # Создание объектов
            #             self.village = village_generation.Village(MAP_SIZE, MAP_SIZE)
            #
            #             # Типы предметов, которые можно класть в слоты снаряжения
            #             allowed_types = [ItemType.Weapon, ItemType.Equipment, ItemType.Equipment,
            #                              ItemType.Equipment, ItemType.Equipment]
            #
            #             self.player = Hero(self.village, MAP_SIZE * 2, Inventory(60, 10),
            #                                Inventory(5, 5, [ITEMS_DB["Sword"]]))
            #
            #             # Инициализация интерфейсов в списке
            #             # # Первый интерфейс - это сам инвентарь
            #             # # Второй - инвентарь снаряжения
            #             self.player_interfaces = [Interface(self.player.inventory, Vector2(5, 5), Vector2(50, 62.5),
            #                                                 InterfaceTypes.Regular),
            #                                       Interface(self.player.equipment_inventory, Vector2(5, 5),
            #                                                 Vector2(50, 875),
            #                                                 InterfaceTypes.Equipment, allowed_types)]
            #
            #             self.camera = Camera()
            #
            #             self.main_game()
            pygame.display.flip()


# Запуск игры
if __name__ == '__main__':
    game = MainGame()
    game.draw_main_menu()
