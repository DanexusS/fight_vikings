from enum import Enum
from items import ItemType


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class Inventory:
    def __init__(self, item_slots):
        self.item_slots = item_slots


class ItemSlot:
    def __init__(self, item, amount, allowed_types=ItemType.Null):
        self.item = item
        self.amount = amount
        self.allowed_types = allowed_types
