from items import *


class IncorrectInventorySize(Exception):
    pass


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class InventorySlot:
    def __init__(self, item: AbstractItem, amount: int, allowed_types: list[ItemType] = None):
        if allowed_types is None:
            allowed_types = []

        self.item = item
        self.amount = amount
        self.allowed_types = allowed_types

    def update_slot(self, _item: AbstractItem = None, _amount: int = 0):
        self.item = _item
        self.amount = _amount

    def add_amount(self, _amount: int):
        self.update_slot(self.item, self.amount + _amount)

    def can_place_in_slot(self, _item: AbstractItem) -> bool:
        if self.allowed_types is None or _item is None or _item.item_id == -1:
            return True
        return _item.item_type in self.allowed_types


class InventoryObject:
    def __init__(self, size: int, item_slots: list[InventorySlot]):
        if len(item_slots) != size:
            raise IncorrectInventorySize

        self.item_slots = item_slots

    def clear(self):
        self.item_slots = []


class Inventory:
    def __init__(self, inventory: InventoryObject):
        self.inventory = inventory
        self.save_path = ""

    def get_slots(self) -> list[InventorySlot]:
        return self.inventory.item_slots

    def empty_slot_count(self) -> int:
        counter = 0

        for slot in self.get_slots():
            if slot.item.item_id == -1:
                counter += 1

        return counter

    def add_item(self, _item: AbstractItem, _amount: int) -> bool:
        if self.empty_slot_count() <= 0:
            return False

        slot = self.find_item_in_inv(_item)

        if slot is None:
            self.set_empty_slot(_item, _amount)
            return True

        slot.add_amount(_amount)
        return True

    def find_item_in_inv(self, _item: AbstractItem):
        for slot in self.get_slots():
            if slot.item.item_id == _item.item_id:
                return slot
        return None

    def set_empty_slot(self, _item: AbstractItem, _amount: int):
        for slot in self.get_slots():
            if slot.item.item_id == -1:
                slot.update_slot(_item, _amount)
                return slot
        return None

    def remove_item(self, _item: AbstractItem):
        for slot in self.get_slots():
            if slot.item == _item:
                slot.update_slot()

    @staticmethod
    def swap_item(_item1: InventorySlot, _item2: InventorySlot):
        if _item2.can_place_in_slot(_item1.item) and _item1.can_place_in_slot(_item2.item):
            temp_slot = InventorySlot(_item2.item, _item2.amount)

            _item2.update_slot(_item1.item, _item1.amount)
            _item1.update_slot(temp_slot.item, temp_slot.amount)
