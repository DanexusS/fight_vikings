from enum import Enum


class Inventory:
    def __init__(self, item_slots):
        self.item_slots = item_slots


class ItemSlot:
    def __init__(self, item, amount):
        self.item = item
        self.amount = amount


class ItemType(Enum):
    Food = 0
    Equipment = 1


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class AbstractItem:
    def __init__(self, item_type, item_id, title):
        self.item_type = item_type
        self.item_id = item_id
        self.title = title


class EquipmentObject(AbstractItem):
    def __init__(self, item_type, item_id, title, *buffs):
        super().__init__(item_type, item_id, title)

        self.type = ItemType.Equipment
        self.buffs = buffs
        self.is_stackable = False


class AbstractUsingItem(AbstractItem):
    def use_item(self):
        pass


class FoodItem(AbstractUsingItem):
    def __init__(self, item_type, item_id, title):
        super().__init__(item_type, item_id, title)

        self.type = ItemType.Food
        self.is_stackable = True

    def use_item(self):
        print("used item food")


class ItemBuff:
    def __init__(self, affected_attribute, value):
        self.affected_attribute = affected_attribute
        self.value = value
