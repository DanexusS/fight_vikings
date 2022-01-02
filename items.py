class Attributes:
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class ItemType:
    Food = 0
    Equipment = 1
    Weapon = 2
    Item = 3


class ItemBuff:
    def __init__(self, affected_attribute: Attributes, value: int):
        self.affected_attribute = affected_attribute
        self.value = value


class AbstractItem:
    def __init__(self, title: str = ""):
        self.ID = -1
        self.TYPE = ItemType.Item
        self.title = title
        self.is_stackable = True
        self.image = None


class FoodItem(AbstractItem):
    def __init__(self, title: str):
        super().__init__(title)

        self.TYPE = ItemType.Food

    def use_item(self):
        print(self.TYPE)


#   КЛАСС СНАРЯЖЕНИЯ
class EquipmentItem(AbstractItem):
    def __init__(self, title: str, durability: int, buff: ItemBuff = None):
        super().__init__(title)

        self.TYPE = ItemType.Equipment
        self.buffs = buff
        self.is_stackable = False
        self.durability = durability


class WeaponItem(EquipmentItem):
    def __init__(self, title: str, durability: int, damage: int, buff: ItemBuff = None, ):
        super().__init__(title, durability, buff)

        self.TYPE = ItemType.Weapon
        self.damage = damage
