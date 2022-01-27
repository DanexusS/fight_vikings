"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Drunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


import csv
import sqlite3
import village_generation

from persons_and_camera import Camera

from player_class import *
from interface import *
from general_stuff import *


class Village:
    def __init__(self, main_game):
        self.houses = {'castle': 1, 'brewery': 1, 'blacksmith': 1, 'tower': 1}
        self.resource = {'gold': 1, 'wood': 1, 'iron': 1}

        self.main_game = main_game

        set_const()
        self.main_game.village = village_generation.Village(MAP_SIZE, MAP_SIZE)

        # Типы предметов, которые можно класть в слоты снаряжения
        allowed_types = [ItemType.Weapon, ItemType.Helmet, ItemType.Chestplate,
                         ItemType.Pants, ItemType.Boots]

        self.main_game.player = Hero(self.main_game.village, MAP_SIZE * 2, Inventory(60, 10),
                                     Inventory(5, 5))

        # Инициализация интерфейсов в списке
        # # Первый интерфейс - это сам инвентарь
        # # Второй - инвентарь снаряжения
        self.main_game.player_interfaces = [Interface(self.main_game.player.inventory,
                                                      Vector2(5, 5), Vector2(50, 62.5),
                                                      InterfaceTypes.Regular),
                                            Interface(self.main_game.player.equipment_inventory,
                                                      Vector2(5, 5),
                                                      Vector2(50, 875),
                                                      InterfaceTypes.Equipment, allowed_types)]

        self.main_game.camera = Camera()

    def add_res(self, amounts):
        for elem in amounts:
            self.resource[elem[0]] += elem[1]

    def upgrade_house(self, name):
        base = self.houses['castle']
        if name == 'cas':
            cur = self.houses['castle']
            if self.resource['gold'] - 100 * cur >= 0 and self.resource['wood'] - 100 * cur >= 0 and \
                    0 <= self.resource['iron'] - 100 * cur:
                self.resource['gold'] -= 100 * cur
                self.resource['wood'] -= 100 * cur
                self.resource['iron'] -= 100 * cur
                self.houses['castle'] += 1
                self.main_game.player.attributes[Attributes.Health].current_value += 15 * self.houses['castle']
        elif name == 'bre':
            cur = self.houses['brewery']
            if self.resource['gold'] - 100 * cur >= 0 and self.resource['wood'] - 50 * cur >= 0 and \
                    self.resource['iron'] - 5 * cur >= 0 and base > cur:
                self.resource['gold'] -= 100 * cur
                self.resource['wood'] -= 50 * cur
                self.resource['iron'] -= 5 * cur
                self.houses['brewery'] += 1
                self.main_game.player.attributes[Attributes.Move_Speed].current_value += 5
        elif name == 'bla':
            cur = self.houses['blacksmith']
            if self.resource['gold'] - 100 * cur >= 0 and self.resource['wood'] - 15 * cur >= 0 and \
                    self.resource['iron'] - 100 * cur >= 0 and base > cur:
                self.resource['gold'] -= 100 * cur
                self.resource['wood'] -= 15 * cur
                self.resource['iron'] -= 100 * cur
                self.houses['blacksmith'] += 1
                self.main_game.player.attributes[Attributes.Armor].current_value += 7.5
        elif name == 'tow':
            cur = self.houses['tower']
            if self.resource['gold'] - 100 * cur >= 0 and self.resource['wood'] - 200 * cur >= 0 and \
                    self.resource['iron'] - 40 * cur >= 0 and base > cur:
                self.resource['gold'] -= 100 * cur
                self.resource['wood'] -= 200 * cur
                self.resource['iron'] -= 40 * cur
                self.houses['tower'] += 1

    def load(self, file_name):
        buildings = ('castle', 'brewery', 'blacksmith', 'tower')
        res = ('gold', 'wood', 'iron')
        with open(file_name, mode='r', newline='') as save:
            read = csv.reader(save, delimiter=';')
            for elem in read:
                if len(elem) == 4:
                    for i in range(0, 4):
                        self.houses[buildings[i]] = int(elem[i])
                else:
                    for i in range(0, 3):
                        self.resource[res[i]] = int(elem[i])

    def save(self, file_name):
        with open(file_name, mode='w', newline='') as save:
            write = csv.writer(save, delimiter=';', quoting=csv.QUOTE_MINIMAL)
            spis = []
            for elem in self.houses.values():
                spis.append(elem)
            write.writerow(spis)
            spis = []
            for elem in self.resource.values():
                spis.append(elem)
            write.writerow(spis)
            save.close()

    def start(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init(channels=1)
        size = width, height = 1920, 1080
        screen = pygame.display.set_mode(size)
        clock = pygame.time.Clock()
        fonts = pygame.font.Font('Vetka.otf', 40)
        values = pygame.font.Font('Vetka.otf', 30)
        village = True
        tab = False
        up = False
        selected = ''
        click = False
        fight = False
        X = 359
        Y = 199
        used = {'gold': 0, 'wood': 0, 'iron': 0}
        self.main_theme = pygame.mixer.Sound('Last_version.wav')

        zamok = pygame.image.load('images/castle.png')
        zamok_clicked = pygame.image.load('images/castle_clicked.png')
        kuznya = pygame.image.load('images/blacksmith.png')
        kuznya_clicked = pygame.image.load('images/blacksmith_clicked.png')
        dungeon = pygame.image.load('images/tower.png')
        dungeon_clicked = pygame.image.load('images/tower_clicked.png')
        pivo = pygame.image.load('images/brewery.png')
        pivo_clicked = pygame.image.load('images/brewery_clicked.png')
        storage = pygame.image.load('images/storage.png')
        upgrade = pygame.image.load('images/upgrade.png')
        anvil = pygame.image.load('images/anvil.png')
        rama = pygame.image.load('images/frames.png')
        res = pygame.image.load('images/resoces.png')
        blacksmth_back = pygame.image.load('images/forge.png')
        plus = pygame.image.load('images/plus.png')
        minus = pygame.image.load('images/minus.png')
        attack = pygame.image.load('images/attack.png')
        escape = pygame.image.load('images/exit_demo.png')
        crafting = pygame.image.load('images/craft_btn.png')
        sprites = pygame.sprite.Group()
        sprites_for_forge = pygame.sprite.Group()

        money_plus = pygame.sprite.Sprite()
        money_plus.image = plus
        money_plus.rect = money_plus.image.get_rect()
        money_plus.rect.x = X + 175
        money_plus.rect.y = Y + 150
        money_plus.add(sprites_for_forge)

        money_minus = pygame.sprite.Sprite()
        money_minus.image = minus
        money_minus.rect = money_minus.image.get_rect()
        money_minus.rect.x = X + 40
        money_minus.rect.y = Y + 150
        money_minus.add(sprites_for_forge)

        wood_plus = pygame.sprite.Sprite()
        wood_plus.image = plus
        wood_plus.rect = wood_plus.image.get_rect()
        wood_plus.rect.x = X + 175
        wood_plus.rect.y = Y + 325
        wood_plus.add(sprites_for_forge)

        wood_minus = pygame.sprite.Sprite()
        wood_minus.image = minus
        wood_minus.rect = wood_minus.image.get_rect()
        wood_minus.rect.x = X + 40
        wood_minus.rect.y = Y + 325
        wood_minus.add(sprites_for_forge)

        iron_plus = pygame.sprite.Sprite()
        iron_plus.image = plus
        iron_plus.rect = iron_plus.image.get_rect()
        iron_plus.rect.x = X + 175
        iron_plus.rect.y = Y + 500
        iron_plus.add(sprites_for_forge)

        iron_minus = pygame.sprite.Sprite()
        iron_minus.image = minus
        iron_minus.rect = iron_minus.image.get_rect()
        iron_minus.rect.x = X + 40
        iron_minus.rect.y = Y + 500
        iron_minus.add(sprites_for_forge)

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
        resorces.add(sprites_for_forge)

        war = pygame.sprite.Sprite()
        war.image = attack
        war.rect = war.image.get_rect()
        war.rect.x = 0
        war.rect.y = Y + 754
        war.add(sprites)

        esc = pygame.sprite.Sprite()
        esc.image = escape
        esc.rect = esc.image.get_rect()
        esc.rect.x = 0
        esc.rect.y = 0
        esc.add(sprites)

        craft = pygame.sprite.Sprite()
        craft.image = crafting
        craft.rect = craft.image.get_rect()
        craft.rect.x = 429
        craft.rect.y = 800
        craft.add(sprites_for_forge)

        def recount():
            nonlocal money, money_pos, woods, woods_pos, iron, iron_pos
            sup = []
            for elem in self.resource.values():
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

        def recount_forge():
            nonlocal money_usage, money_usage_pos, woods_usage, woods_usage_pos, iron_usage, iron_usage_pos
            sup = []
            for elem in used.values():
                if elem >= 1000000:
                    sup.append(f'{elem // 1000000}M')
                elif elem >= 1000:
                    sup.append(f'{elem // 1000}K')
                else:
                    sup.append(str(elem))

            money_usage = values.render(sup[0], True, (255, 0, 0))
            money_usage_pos = money_usage.get_rect()
            money_usage_pos.center = (495, 378)

            woods_usage = values.render(sup[1], True, (255, 0, 0))
            woods_usage_pos = woods_usage.get_rect()
            woods_usage_pos.center = (495, 555)

            iron_usage = values.render(sup[2], True, (255, 0, 0))
            iron_usage_pos = iron_usage.get_rect()
            iron_usage_pos.center = (495, 730)

        money = values.render('', True, (255, 0, 0))
        money_pos = money.get_rect()
        money_pos.center = (X + 1329, 97)

        woods = values.render('', True, (255, 0, 0))
        woods_pos = woods.get_rect()
        woods_pos.center = (X + 1420, 97)

        iron = values.render('', True, (255, 0, 0))
        iron_pos = iron.get_rect()
        iron_pos.center = (X + 1518, 97)

        money_usage = values.render('0', True, (255, 0, 0))
        money_usage_pos = money_usage.get_rect()
        money_usage_pos.center = (495, 378)

        woods_usage = values.render('0', True, (255, 0, 0))
        woods_usage_pos = woods_usage.get_rect()
        woods_usage_pos.center = (495, 555)

        iron_usage = values.render('0', True, (255, 0, 0))
        iron_usage_pos = iron_usage.get_rect()
        iron_usage_pos.center = (495, 730)

        recount()

        top_frame = fonts.render('', True, (255, 0, 0))
        top_frame_pos = top_frame.get_rect()
        top_frame_pos.center = (X + 50, 25)

        bottom_frame = fonts.render('', True, (255, 0, 0))
        bottom_frame_pos = bottom_frame.get_rect()
        bottom_frame_pos.center = (1000, Y + 335)

        def forging():
            if self.resource['gold'] - used['gold'] >= 0 and self.resource['wood'] - used['wood'] >= 0 and \
                    self.resource['iron'] - used['iron'] >= 0:
                spis = []
                con = sqlite3.connect('items_db.sqlite')
                cur = con.cursor()
                for i in range(-5, 5):
                    find = (str(used['gold'] + i), str(used['wood'] + i), str(used['iron'] + i))
                    finded = cur.execute("""SELECT * From items WHERE craft = ?""", (';'.join(find),))
                    for elem in finded:
                        spis.append(elem)
                if len(spis) > 0:
                    forged = spis[-1]
                    used_in = forged[8].split(';')
                    self.resource['gold'] -= int(used_in[0])
                    self.resource['wood'] -= int(used_in[1])
                    self.resource['iron'] -= int(used_in[2])
                # АХТУНГА НУЖЕН ДАНЕКСУС С ИНВЕНТАРЁМ
                recount()

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
            if village:
                screen.blit(image, (0, 0))
                sprites.draw(screen)
                screen.blit(top_frame, top_frame_pos)
                screen.blit(bottom_frame, bottom_frame_pos)
            else:
                screen.blit(blacksmth_back, (0, 0))
                sprites_for_forge.draw(screen)
                screen.blit(money_usage, money_usage_pos)
                screen.blit(woods_usage, woods_usage_pos)
                screen.blit(iron_usage, iron_usage_pos)
                recount_forge()
            screen.blit(money, money_pos)
            screen.blit(woods, woods_pos)
            screen.blit(iron, iron_pos)
        self.main_theme.play(-1, 0, 500)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        tab = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_TAB:
                        tab = False
                    if event.key == pygame.K_ESCAPE:
                        if not village:
                            village = True
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
                cur_pos = pygame.mouse.get_pos()
                if village:
                    if castle.rect.collidepoint(cur_pos):
                        standart()
                        set_top('Замок - место где хранятся награбленные богатства, и проводятся шумные пиры')
                        lvl = self.houses['castle']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {100 * lvl} wood {100 * lvl} iron')
                        selected = 'cas'
                        standart_castle = zamok_clicked
                    elif blacksmith.rect.collidepoint(cur_pos):
                        standart()
                        set_top('Кузница - место где ваших воинов снаряжают оружием и доспехами')
                        lvl = self.houses['blacksmith']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {15 * lvl} wood {100 * lvl} iron')
                        selected = 'bla'
                        standart_blacksmith = kuznya_clicked
                    elif tower.rect.collidepoint(cur_pos):
                        standart()
                        set_top('Башня - место где ваши воины отдыхают в перерывах между набегами')
                        lvl = self.houses['tower']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {200 * lvl} wood {40 * lvl} iron')
                        selected = 'tow'
                        standart_tower = dungeon_clicked
                    elif brewery.rect.collidepoint(cur_pos):
                        standart()
                        set_top('Пивоварня - ничто так не поднимает настроение, как кружка пенного! Скёль!')
                        lvl = self.houses['brewery']
                        set_bottom(f'Lvl {lvl}. Для улучшения: {100 * lvl} gold {50 * lvl} wood {5 * lvl} iron')
                        selected = 'bre'
                        standart_brewery = pivo_clicked
                    elif up_btn.rect.collidepoint(cur_pos):
                        up = True
                    elif forge.rect.collidepoint(cur_pos):
                        village = False
                    elif war.rect.collidepoint(cur_pos):
                        fight = True
                    elif esc.rect.collidepoint(cur_pos):
                        screen.fill(BG_COLOR)
                        self.save('save.csv')
                        self.main_theme.stop()
                        self.main_game.draw_main_menu()
                    elif backpack.rect.collidepoint(cur_pos):
                        screen.fill(BG_COLOR)
                        self.save('save.csv')
                        self.main_game.on_inventory_open(1)
                    else:
                        set_top('')
                        set_bottom('')
                        standart_castle = zamok
                        standart_blacksmith = kuznya
                        standart_tower = dungeon
                        standart_brewery = pivo
                else:
                    if money_plus.rect.collidepoint(cur_pos):
                        used['gold'] += 1
                    elif money_minus.rect.collidepoint(cur_pos):
                        used['gold'] -= 1
                    elif wood_plus.rect.collidepoint(cur_pos):
                        used['wood'] += 1
                    elif wood_minus.rect.collidepoint(cur_pos):
                        used['wood'] -= 1
                    elif iron_plus.rect.collidepoint(cur_pos):
                        used['iron'] += 1
                    elif iron_minus.rect.collidepoint(cur_pos):
                        used['iron'] -= 1
                    elif craft.rect.collidepoint(cur_pos):
                        forging()
                    recount_forge()
                click = False

                if up:
                    if village:
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

                if fight:
                    thread = threading.Thread(target=self.main_game.draw_load)
                    thread.daemon = True
                    thread.start()

                    self.save('save.csv')
                    self.main_game.main_game()

            update()
            clock.tick(20)
            pygame.display.flip()
