import pygame
import sys
import threading

import village_generation
import player_and_camera

# Создание окна pygame
pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption('Fight Vikings')

# Константы
BG = '#43485E'
BG_BTN = '#C8D1F7'
BG_BTN_SHADOW = '#242429'
SIZE_BTN_MENU = (300, 80)
FONT_BTN = pygame.font.SysFont('Corbel', 50)
FONT_LOAD = pygame.font.SysFont('Impact', 60)

# Позиции кнопок в меню
pos_exit = (width // 2 - SIZE_BTN_MENU[0] // 2, height // 2 + 300 - SIZE_BTN_MENU[1] // 2)
pos_play = (width // 2 - SIZE_BTN_MENU[0] // 2, height // 2 + 200 - SIZE_BTN_MENU[1] // 2)

# Фон
screen.fill(BG)

# Игра
class MainGame:
    def draw_menu(self):
        # Кнопка выход
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_exit[0] - 4, pos_exit[1] + 4, SIZE_BTN_MENU[0], SIZE_BTN_MENU[1]))
        pygame.draw.rect(screen, BG_BTN, (pos_exit[0], pos_exit[1], SIZE_BTN_MENU[0], SIZE_BTN_MENU[1]))
        screen.blit(FONT_BTN.render('Выход', True, (0, 0, 0)), (pos_exit[0] + 80, pos_exit[1] + 18))

        # Кнопка начать игру
        pygame.draw.rect(screen, BG_BTN_SHADOW, (pos_play[0] - 4, pos_play[1] + 4, SIZE_BTN_MENU[0], SIZE_BTN_MENU[1]))
        pygame.draw.rect(screen, BG_BTN, (pos_play[0], pos_play[1], SIZE_BTN_MENU[0], SIZE_BTN_MENU[1]))
        screen.blit(FONT_BTN.render('Играть', True, (0, 0, 0)), (pos_play[0] + 80, pos_play[1] + 18))

        # Обновить
        pygame.display.flip()

    def draw_load(self):
        screen.fill(BG)
        screen.blit(FONT_LOAD.render('Загрузка...', True, BG_BTN), (width // 2 - 120, height // 2))
        pygame.display.flip()

    def game(self):
        screen.fill(BG)

        pygame.mouse.set_visible(False)

        # Создание объектов
        village = village_generation.Village(village_generation.N, village_generation.N)
        player = player_and_camera.Hero(village, village_generation.N * 2)
        camera = player_and_camera.Camera()

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(BG)
                        self.menu()

                player.update(event, screen)

            for direction in player.directions.items():
                player.move_player(direction, village)

            camera.update(player, width, height)
            for sprite in village.all_sprites:
                camera.apply(sprite)

            village.render(screen)
            pygame.display.flip()

    def menu(self):
        pygame.mouse.set_visible(True)

        # Создание объектов
        threading.Thread(target=self.draw_menu).start()

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_x = pygame.mouse.get_pos()[0]
                    mouse_y = pygame.mouse.get_pos()[1]
                    if mouse_x >= pos_exit[0] and mouse_y >= pos_exit[1] and \
                            (mouse_x <= pos_exit[0] + SIZE_BTN_MENU[0] and mouse_y <= pos_exit[1] + SIZE_BTN_MENU[1]):
                        sys.exit()
                    if mouse_x >= pos_play[0] and mouse_y >= pos_play[1] and \
                            (mouse_x <= pos_play[0] + SIZE_BTN_MENU[0] and mouse_y <= pos_play[1] + SIZE_BTN_MENU[1]):
                        t = threading.Thread(target=self.draw_load())
                        t.daemon = True
                        t.start()
                        self.game()
            pygame.display.flip()

# Запуск игры
if __name__ == '__main__':
    game = MainGame()
    game.menu()
