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
    Armor = 1


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class AbstractItem:
    def __init__(self, item_type, is_stackable, item_id, title):
        self.item_type = item_type
        self.is_stackable = is_stackable
        self.item_id = item_id
        self.title = title


class AbstractUsingItem(AbstractItem):
    def use_item(self):
        pass


class FoodItem(AbstractUsingItem):
    def __init__(self, item_type, is_stackable, item_id, title):
        super().__init__(item_type, is_stackable, item_id, title)

        self.type = ItemType.Food

    def use_item(self):
        print("used item food")


class ItemBuff:
    def __init__(self, value, affected_attributes):
        self.affected_attributes = affected_attributes
        self.value = value


for shake in ItemType:
    print(shake)
