from enum import Enum


class ItemType(Enum):
    Null = -1
    Food = 0
    Equipment = 1
    Weapon = 2
    Potion = 3


class AbstractItem:
    def __init__(self, item_id, title):
        self.item_id = item_id
        self.title = title
        self.is_stackable = True


class AbstractUsingItem(AbstractItem):
    def __init__(self, item_id, title, use_key):
        super().__init__(item_id, title)

        self.use_key = use_key

    def use_item(self):
        pass


#   КЛАСС СНАРЯЖЕНИЯ
class EquipmentObject(AbstractItem):
    def __init__(self, item_type, item_id, title, buffs, durability):
        super().__init__(item_id, title)

        self.type = item_type
        self.buffs = buffs
        self.is_stackable = False
        self.durability = durability


#   КЛАСС ЕДЫ
class FoodObject(AbstractUsingItem):
    def __init__(self, item_id, title, use_key):
        super().__init__(item_id, title, use_key)

        self.type = ItemType.Food

    def use_item(self):
        print("used item food")


class PotionObject(AbstractUsingItem):
    def __init__(self, item_id, title, use_key, buff):
        super().__init__(item_id, title, use_key)

        self.type = ItemType.Potion
        self.buff = buff


class ItemBuff:
    def __init__(self, affected_attribute, value):
        self.affected_attribute = affected_attribute
        self.value = value
