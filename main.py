import pygame

# Создание окна pygame
pygame.init()
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
pygame.display.set_caption('Fight Vikings')

# Фон
screen.fill((220, 220, 200))

# Переменные
size_btn = (300, 80)
font_btn = pygame.font.SysFont('Corbel', 50)

# Кнопка выход
pos_exit = (width // 2 - size_btn[0] // 2, height // 2 + 300 - size_btn[1] // 2)
button_exit = pygame.draw.rect(screen, (200, 100, 100), (pos_exit[0], pos_exit[1], size_btn[0], size_btn[1]))
screen.blit(font_btn.render('Выход', True, (0, 0, 0)), (pos_exit[0] + 80, pos_exit[1] + 18))

# Кнопка начать игру
pos_play = (width // 2 - size_btn[0] // 2, height // 2 + 200 - size_btn[1] // 2)
button_play = pygame.draw.rect(screen, (100, 100, 100), (pos_play[0], pos_play[1], size_btn[0], size_btn[1]))
screen.blit(font_btn.render('Играть', True, (0, 0, 0)), (pos_play[0] + 80, pos_play[1] + 18))

# Обновить
pygame.display.flip()

# Игра
def game():
    # Сделать цикл игры
    print('w')

# Меню
def menu():
    running_menu = True
    while running_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_menu = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                if mouse_x >= pos_exit[0] and mouse_y >= pos_exit[1] and \
                        (mouse_x <= pos_exit[0] + size_btn[0] and mouse_y <= pos_exit[1] + size_btn[1]):
                    running_menu = False
                if mouse_x >= pos_play[0] and mouse_y >= pos_play[1] and \
                        (mouse_x <= pos_play[0] + size_btn[0] and mouse_y <= pos_play[1] + size_btn[1]):
                    game()
        pygame.display.flip()

# Запуск игры
if __name__ == '__main__':
    menu()
