from main_functions import *


class Weapon(pygame.sprite.Sprite):
    def __init__(self, village, name_weapon):
        super().__init__(village.sword_sprites)
        # Переменные
        self.image = pygame.transform.rotate(pygame.transform.scale(load_image(f"{name_weapon}.png"),
                                                                    (PLAYER_SIZE - 10, PLAYER_SIZE - 10)), 180)
        self.rect = self.image.get_rect()

    def rotate(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.x, mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, int(angle))
        return angle

    def attack(self, dmg, village, target=False):
        # Если соприкосаеться с объектом - удар
        objs_collide = []
        for sprite in village.collide_sprites:
            if pygame.sprite.collide_mask(self, sprite) and (not target or (sprite.__class__.__name__ == target)):
                obj = sprite
                objs_collide.append(obj)
                # Бьёт 1 раз
                if not obj.is_dmg:
                    status = obj.damage(dmg)
                    if obj.__class__.__name__ in ['Enemy', 'Hero'] and str(status) in ['destroyed', 'PlayerStates.Dead']:
                        obj.kill()
                        if obj.weapon:
                            village.sword_sprites.remove(obj.weapon)
                            obj.weapon.kill()
        # Перезагрузка удара
        for sprite in village.collide_sprites:
            if sprite not in objs_collide:
                sprite.is_dmg = False
