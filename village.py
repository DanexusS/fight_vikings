"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import pygame


class Village:
    def __init__(self):
        self.houses = {'castle': 1, 'brewery': 1, 'blacksmith': 1, 'tower': 1}
        self.resoces = {'gold': 1000000, 'wood': 10000000, 'iron': 1000000000}

    def add_res(self, amounts):
        for elem in amounts:
            self.resoces[elem[0]] += elem[1]

    def upgrade_house(self, name):
        base = self.houses['castle']
        if name == 'cas':
            cur = self.houses['castle']
            if self.resoces['gold'] - 100 * cur >= 0 and self.resoces['wood'] - 100 * cur >= 0 and \
            0 <= self.resoces['iron'] - 100 * cur:
                self.resoces['gold'] -= 100 * cur
                self.resoces['wood'] -= 100 * cur
                self.resoces['iron'] -= 100 * cur
                self.houses['castle'] += 1
        elif name == 'bre':
            cur = self.houses['brewery']
            if self.resoces['gold'] - 100 * cur >= 0 and self.resoces['wood'] - 50 * cur >= 0 and \
            self.resoces['iron'] - 5 * cur >= 0 and base > cur:
                self.resoces['gold'] -= 100 * cur
                self.resoces['wood'] -= 50 * cur
                self.resoces['iron'] -= 5 * cur
                self.houses['brewery'] += 1
        elif name == 'bla':
            cur = self.houses['blacksmith']
            if self.resoces['gold'] - 100 * cur >= 0 and self.resoces['wood'] - 15 * cur >= 0 and \
            self.resoces['iron'] - 100 * cur >=0 and base > cur:
                self.resoces['gold'] -= 100 * cur
                self.resoces['wood'] -= 15 * cur
                self.resoces['iron'] -= 100 * cur
                self.houses['blacksmith'] += 1
        elif name == 'tow':
            cur = self.houses['tower']
            if self.resoces['gold'] - 100 * cur >= 0 and self.resoces['wood'] - 200 * cur >= 0 and \
            self.resoces['iron'] - 40 * cur >= 0 and base > cur:
                self.resoces['gold'] -= 100 * cur
                self.resoces['wood'] -= 200 * cur
                self.resoces['iron'] -= 40 * cur
                self.houses['tower'] += 1

    def load(self, file_name):
        pass

    def start(self):
        pygame.init()
        pygame.font.init()
        size = width, height = 1920, 1080
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        fonts = pygame.font.Font('Vetka.otf', 40)
        tab = False
        up = False
        selected = ''
        click = False
        X = 359
        Y = 199

        zamok = pygame.image.load('images/castle.png')
        zamok_clicked = pygame.image.load('images\\castle_clicked.png')
        kuznya = pygame.image.load('images\\blacksmith.png')
        kuznya_clicked = pygame.image.load('images\\blacksmith_clicked.png')
        dungeon = pygame.image.load('images\\tower.png')
        dungeon_clicked = pygame.image.load('images\\tower_clicked.png')
        pivo = pygame.image.load('images\\brewery.png')
        pivo_clicked = pygame.image.load('images\\brewery_clicked.png')
        storage = pygame.image.load('images\\storage.png')
        upgrade = pygame.image.load('images\\upgrade.png')
        anvil = pygame.image.load('images\\anvil.png')
        rama = pygame.image.load('images\\frames.png')
        res = pygame.image.load('images\\resoces.png')
        sprites = pygame.sprite.Group()

        standart_castle = zamok
        standart_blacksmith = kuznya
        standart_tower = dungeon
        standart_brewery = pivo

        forge = pygame.sprite.Sprite()
        forge.image = anvil
        forge.rect = forge.image.get_rect()
        forge.rect.x = 0
        forge.rect.y = 219
        forge.add(sprites)

        up_btn = pygame.sprite.Sprite()
        up_btn.image = upgrade
        up_btn.rect = up_btn.image.get_rect()
        up_btn.rect.x = X + 1337
        up_btn.rect.y = Y + 228
        up_btn.add(sprites)

        backpack = pygame.sprite.Sprite()
        backpack.image = storage
        backpack.rect = backpack.image.get_rect()
        backpack.rect.x = X + 1337
        backpack.rect.y = Y + 20
        backpack.add(sprites)

        castle = pygame.sprite.Sprite()
        castle.image = zamok
        castle.rect = castle.image.get_rect()
        castle.rect.x = X + 729
        castle.rect.y = Y + 207
        castle.add(sprites)

        blacksmith = pygame.sprite.Sprite()
        blacksmith.image = kuznya
        blacksmith.rect = blacksmith.image.get_rect()
        blacksmith.rect.x = X + 283
        blacksmith.rect.y = Y + 324
        blacksmith.add(sprites)

        tower = pygame.sprite.Sprite()
        tower.image = dungeon
        tower.rect = tower.image.get_rect()
        tower.rect.x = X + 140
        tower.rect.y = Y + 134
        tower.add(sprites)

        brewery = pygame.sprite.Sprite()
        brewery.image = pivo
        brewery.rect = brewery.image.get_rect()
        brewery.rect.x = X + 837
        brewery.rect.y = Y + 420
        brewery.add(sprites)

        frame = pygame.sprite.Sprite()
        frame.image = rama
        frame.rect = frame.image.get_rect()
        frame.rect.x = 0
        frame.rect.y = 0
        frame.add(sprites)

        resorces = pygame.sprite.Sprite()
        resorces.image = res
        resorces.rect = resorces.image.get_rect()
        resorces.rect.x = X + 1291
        resorces.rect.y = 0
        resorces.add(sprites)
        def recount():
            nonlocal money, money_pos, woods, woods_pos, iron, iron_pos
            sup = []
            for elem in self.resoces.values():
                if elem >= 1000000:
                    sup.append(f'{elem // 1000000}M')
                elif elem >= 1000:
                    sup.append(f'{elem // 1000}K')
                else:
                    sup.append(str(elem))

            money = pygame.font.Font('Vetka.otf', 30).render(sup[0], True, (255, 0, 0))
            money_pos = money.get_rect()
            money_pos.center = (X + 1329, 97)

            woods = pygame.font.Font('Vetka.otf', 30).render(sup[1], True, (255, 0, 0))
            woods_pos = woods.get_rect()
            woods_pos.center = (X + 1420, 97)

            iron = pygame.font.Font('Vetka.otf', 30).render(sup[2], True, (255, 0, 0))
            iron_pos = iron.get_rect()
            iron_pos.center = (X + 1518, 97)

        money = pygame.font.Font('Vetka.otf', 30).render('', True, (255, 0, 0))
        money_pos = money.get_rect()
        money_pos.center = (X + 1329, 97)

        woods = pygame.font.Font('Vetka.otf', 30).render('', True, (255, 0, 0))
        woods_pos = woods.get_rect()
        woods_pos.center = (X + 1420, 97)

        iron = pygame.font.Font('Vetka.otf', 30).render('', True, (255, 0, 0))
        iron_pos = iron.get_rect()
        iron_pos.center = (X + 1518, 97)

        recount()

        top_frame = fonts.render('', True, (255, 0, 0))
        top_frame_pos = top_frame.get_rect()
        top_frame_pos.center = (X + 50, 25)

        bottom_frame = fonts.render('', True, (255, 0, 0))
        bottom_frame_pos = bottom_frame.get_rect()
        bottom_frame_pos.center = (1000, Y + 335)

        def set_top(text):
            nonlocal top_frame_pos, top_frame
            top_frame = fonts.render(text, True, (255, 0, 0))
            top_frame_pos = top_frame.get_rect()
            top_frame_pos.center = (X + 601, 45)

        def set_bottom(text):
            nonlocal bottom_frame, bottom_frame_pos
            bottom_frame = fonts.render(text, True, (255, 0, 0))
            bottom_frame_pos = bottom_frame.get_rect()
            bottom_frame_pos.center = (X + 601, Y + 820)

        image = pygame.image.load('images/main.png')
        screen.blit(image, (0, 0))
        sprites.draw(screen)

        def standart():
            nonlocal standart_castle, standart_tower, standart_blacksmith, standart_brewery
            standart_castle = zamok
            standart_blacksmith = kuznya
            standart_tower = dungeon
            standart_brewery = pivo

        def update():
            screen.blit(image, (0, 0))
            sprites.draw(screen)
            screen.blit(top_frame, top_frame_pos)
            screen.blit(bottom_frame, bottom_frame_pos)
            screen.blit(money, money_pos)
            screen.blit(woods, woods_pos)
            screen.blit(iron, iron_pos)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        tab = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            if tab:
                castle.image = zamok_clicked
                blacksmith.image = kuznya_clicked
                tower.image = dungeon_clicked
                brewery.image = pivo_clicked
            if not tab:
                castle.image = standart_castle
                blacksmith.image = standart_blacksmith
                tower.image = standart_tower
                brewery.image = standart_brewery

            if click:
                if castle.rect.collidepoint(pygame.mouse.get_pos()):
                    standart()
                    set_top('Замок - место где хранятся награбленные богатства, и проводятся шумные пиры')
                    lvl = self.houses['castle']
                    set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {100 * lvl} wood {100 * lvl} iron')
                    selected = 'cas'
                    standart_castle = zamok_clicked
                elif blacksmith.rect.collidepoint(pygame.mouse.get_pos()):
                    standart()
                    set_top('Кузница - место где ваших воинов снаряжают оружием и доспехами')
                    lvl = self.houses['blacksmith']
                    set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {15 * lvl} wood {100 * lvl} iron')
                    selected = 'bla'
                    standart_blacksmith = kuznya_clicked
                elif tower.rect.collidepoint(pygame.mouse.get_pos()):
                    standart()
                    set_top('Башня - место где ваши воины отдыхают в перерывах между набегами')
                    lvl = self.houses['tower']
                    set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {200 * lvl} wood {40 * lvl} iron')
                    selected = 'tow'
                    standart_tower = dungeon_clicked
                elif brewery.rect.collidepoint(pygame.mouse.get_pos()):
                    standart()
                    set_top('Пивоварня - ничто так не поднимает настроение, как кружка пенного! Скёль!')
                    lvl = self.houses['brewery']
                    set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {50 * lvl} wood {5 * lvl} iron')
                    selected = 'bre'
                    standart_brewery = pivo_clicked
                elif up_btn.rect.collidepoint(pygame.mouse.get_pos()):
                    up = True
                else:
                    set_top('')
                    set_bottom('')
                    standart_castle = zamok
                    standart_blacksmith = kuznya
                    standart_tower = dungeon
                    standart_brewery = pivo
                click = False

                if up:
                    self.upgrade_house(selected)
                    recount()
                    if selected == 'cas':
                        lvl = self.houses['castle']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {100 * lvl} wood {100 * lvl} iron')
                    elif selected == 'bre':
                        lvl = self.houses['brewery']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {50 * lvl} wood {5 * lvl} iron')
                    elif selected == 'bla':
                        lvl = self.houses['blacksmith']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {15 * lvl} wood {100 * lvl} iron')
                    elif selected == 'tow':
                        lvl = self.houses['tower']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {200 * lvl} wood {40 * lvl} iron')
                    up = False

            update()
            clock.tick(15)
            pygame.display.flip()


a = Village()
a.start()
