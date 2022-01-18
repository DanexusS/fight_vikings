import sys
import threading
import item_database
import persons_and_camera
import village_generation

from player_class import Hero
from interface import *
from constants import *


# Создание окна pygame
pygame.init()
items_db = item_database.init()

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
        screen.fill(BG)
        screen.blit(FONT_LOAD.render('Загрузка...', True, BG_BTN), (width // 2 - 120, height // 2))
        pygame.display.flip()

    def inventory_opened(self):
        player_interfaces = [Interface(self.player.inventory, Vector2(5, 5),
                                       Vector2(50, 62.5), InterfaceTypes.Regular),
                             Interface(self.player.equipment_inventory,
                                       Vector2(5, 5), Vector2(50, 875), InterfaceTypes.Equipment)]
        threading.Thread(target=player_interfaces[0].render_slots(screen)).start()
        running_inv = True
        while running_inv:
            for event in pygame.event.get():
                if MOUSE.current_interface:
                    if event.type == pygame.QUIT:
                        running_inv = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        MOUSE.current_interface.slot_clicked(event.pos)
                    elif event.type == pygame.MOUSEMOTION:
                        MOUSE.current_interface.mouse_move(event.pos)
                    elif event.type == pygame.MOUSEBUTTONUP:
                        MOUSE.current_interface.drop_item(event.pos)
                    elif event.type == pygame.KEYUP:
                        if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                            if MOUSE.slot_hovered_over:
                                MOUSE.slot_hovered_over.mouse_hovered = False
                            MOUSE.slot_hovered_over = None
                            self.main_game()

            MOUSE.position = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

            screen.fill(BG_COLOR)
            # Отрисовка слотов у инвентарей и проверка на перекрытие их мышкой
            for interface in player_interfaces:
                interface.interface_check()
                interface.render_slots(screen)

            # Перемещение изображения предмета во временя перетаскивания
            if MOUSE.start_drag_slot:
                image = pygame.image.load(MOUSE.start_drag_slot.ui_display)
                slot_image = pygame.transform.scale(image.convert_alpha(), (96, 96))
                rect = slot_image.get_rect(center=MOUSE.position)
                screen.blit(slot_image, rect)
            pygame.display.flip()

    def main_game(self):
        screen.fill(BG)

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(BG)
                        self.menu_opened()
                    if event.key == pygame.K_i:
                        screen.fill(BG_COLOR)
                        self.inventory_opened()

                self.player.update(event)

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

            self.village.render(screen)
            pygame.display.flip()

    @staticmethod
    def button_hover(mouse_pos: Vector2):
        if pos_exit[0] <= mouse_pos.x <= pos_exit[0] + SIZE_MENU_BTN.x and \
                pos_exit[1] <= mouse_pos.y <= pos_exit[1] + SIZE_MENU_BTN.y:
            return "Exit"
        if pos_play[0] <= mouse_pos.x <= pos_play[0] + SIZE_MENU_BTN.x and \
                pos_play[1] <= mouse_pos.y <= pos_play[1] + SIZE_MENU_BTN.y:
            return "Play"

        return None

    def menu_opened(self):
        # Создание объектов
        threading.Thread(target=self.draw_menu).start()

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    button = self.button_hover(mouse_pos)

                    if button == "Exit":
                        sys.exit()
                    if button == "Play":
                        thread = threading.Thread(target=self.draw_load())
                        thread.daemon = True
                        thread.start()

                        # Создание объектов
                        self.village = village_generation.Village(MAP_SIZE, MAP_SIZE)
                        self.player = Hero(self.village, MAP_SIZE * 2,
                                           Inventory(60, 10), Inventory(5, 5, [items_db["Sword"]]))
                        self.camera = persons_and_camera.Camera()

                        self.main_game()
            pygame.display.flip()


# Запуск игры
if __name__ == '__main__':
    game = MainGame()
    game.menu_opened()
