import pygame
import sys

import village_generation

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

# Позиции кнопок в меню
pos_exit = (width // 2 - SIZE_BTN_MENU[0] // 2, height // 2 + 300 - SIZE_BTN_MENU[1] // 2)
pos_play = (width // 2 - SIZE_BTN_MENU[0] // 2, height // 2 + 200 - SIZE_BTN_MENU[1] // 2)

# Фон
screen.fill(BG)

# Игра
class MainGame:
    def draw_btn_menu(self):
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

    def game(self):
        screen.fill(BG)

        village = village_generation.Village(village_generation.N, village_generation.N)

        running_menu = True
        while running_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_menu = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        screen.fill(BG)
                        self.menu()

            village.render(screen)
            pygame.display.flip()

    def menu(self):
        self.draw_btn_menu()

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
                        self.game()
            pygame.display.flip()

# Запуск игры
if __name__ == '__main__':
    game = MainGame()
    game.menu()
