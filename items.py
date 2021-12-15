from enum import Enum


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class ItemType(Enum):
    Null = -1
    Food = 0
    Equipment = 1
    Weapon = 2
    Potion = 3


class ItemBuff:
    def __init__(self, affected_attribute: Attributes, value: int):
        self.affected_attribute = affected_attribute
        self.value = value


class AbstractItem:
    def __init__(self, item_id: int, title: str):
        self.ID = item_id
        self.TYPE = ItemType.Null
        self.title = title
        self.is_stackable = True


class AbstractUsingItem(AbstractItem):
    def __init__(self, item_id: int, title: str, use_key):
        super().__init__(item_id, title)

        self.use_key = use_key

    def use_item(self):
        pass


#   КЛАСС СНАРЯЖЕНИЯ
class EquipmentObject(AbstractItem):
    def __init__(self, item_type: ItemType, item_id: int, title: str, durability: int, buffs: list[ItemBuff] = None):
        super().__init__(item_id, title)

        self.TYPE = item_type
        self.buffs = buffs
        self.is_stackable = False
        self.durability = durability


#   КЛАСС ЕДЫ
class FoodObject(AbstractUsingItem):
    def __init__(self, item_id: int, title: str, use_key):
        super().__init__(item_id, title, use_key)

        self.TYPE = ItemType.Food

    def use_item(self):
        print("used item food")


class PotionObject(AbstractUsingItem):
    def __init__(self, item_id: int, title: str, use_key, buff: ItemBuff):
        super().__init__(item_id, title, use_key)

        self.TYPE = ItemType.Potion
        self.buff = buff
