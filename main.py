"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import sys

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
FONT_C = pygame.font.SysFont('Impact', 20)

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

    def draw_complete(self):
        surf = load_image('bg_complete.png')
        rect = surf.get_rect()
        screen.blit(surf, rect)

        # Кнопка выход
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_exit[0] - 4, pos_exit[1] + 4, SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        pygame.draw.rect(screen, BG_BTN, (pos_exit[0], pos_exit[1], SIZE_MENU_BTN.x, SIZE_MENU_BTN.y))
        screen.blit(FONT_BTN.render('Выход', True, (0, 0, 0)), (pos_exit[0] + 85, pos_exit[1] + 10))

        # Отображение информации
        screen.blit(FONT_C.render(f"+{self.village.gold}", True, (0, 240, 0)), (1670, 85))
        screen.blit(FONT_C.render(f"+{self.village.tree}", True, (0, 240, 0)), (1765, 85))
        screen.blit(FONT_C.render(f"+{self.village.metal}", True, (0, 240, 0)), (1865, 85))

    def inventory_opened(self, from_main_base):
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
                        self.on_inventory_close(self.player_interfaces, from_main_base)

            MOUSE.position = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            screen.fill(BG_COLOR)
            # Отрисовка слотов у инвентарей и проверка на перекрытие их мышкой
            for interface in self.player_interfaces:
                interface.interface_check()
                interface.render_slots(screen)

            # Отображение всех характеристик героя
            y = 0
            for key, value in self.player.attributes.items():
                text = ATTRIBUTE_FONT.render(f"{RUS_ATTRIBUTES[key].capitalize()} -> {round(value.current_value, 2)}",
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

    def on_inventory_close(self, interfaces, from_main_base):
        i = 0
        for interface in interfaces:
            interface.save(i)
            i += 1
        if from_main_base:
            self.main_village.load('save.csv')
            self.main_village.start()
        else:
            self.main_game()

    def on_inventory_open(self, from_n=0):
        fieldnames = ["item", "amount"]

        for i in range(len(self.player_interfaces)):
            file = open(f"saves/inventory_{i}.csv", newline="")
            reader = list(DictReader(file, fieldnames, delimiter=";", quoting=QUOTE_NONNUMERIC))[1:]
            row_count = len(self.player_interfaces[i].inventory.slots[0])
            row = 0
            column = 0
            for line in reader:
                if row >= row_count:
                    row -= row // row_count * row_count
                    column += 1

                if line["item"] != "":
                    slot = InventorySlot(ITEMS_DB[line["item"]], int(line["amount"]))
                    self.player_interfaces[i].inventory.set_slot(row, column, slot)

                row += 1

        self.inventory_opened(from_n)

    def main_game(self):
        screen.fill(BG)

        running_game = True
        while running_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        self.main_village.main_theme.stop()
                        self.main_village.load('save.csv')
                        self.main_village.start()
                    if event.key == pygame.K_i and self.player.state != PlayerStates.Dead:
                        screen.fill(BG_COLOR)
                        self.on_inventory_open(0)
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    if (self.player.state == PlayerStates.Dead or self.village.Town_Hall.status == 'destroed') and \
                            pos_exit[0] <= mouse_pos.x <= pos_exit[0] + SIZE_MENU_BTN.x and \
                            pos_exit[1] <= mouse_pos.y <= pos_exit[1] + SIZE_MENU_BTN.y:
                        self.main_village.main_theme.stop()
                        if self.player.state == PlayerStates.Dead:
                            self.main_village.load('save.csv')
                        self.main_village.start()

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

            # Отображение экрана завершения миссии, если игрок разрушил ратушу
            if self.village.Town_Hall.status == 'destroed':
                self.draw_complete()
            # Отображение экрана смерти, если игрок умер
            elif self.player.state == PlayerStates.Dead:
                self.draw_died()

            # Обновление экрана
            pygame.display.flip()
            pygame.time.delay(20)

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

                        self.main_village = Village(self)
                        self.main_village.load('save.csv')
                        self.main_village.start()
            pygame.display.flip()


# Запуск игры
if __name__ == '__main__':
    game = MainGame()
    game.draw_main_menu()
