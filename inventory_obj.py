from items import *


class IncorrectInventorySize(Exception):
    pass


class InventorySlot:
    def __init__(self, item: AbstractItem, amount: int, allowed_types: list[ItemType] = None):
        if allowed_types is None:
            allowed_types = []

        self.item = item
        self.amount = amount
        self.allowed_types = allowed_types
        self.parent = None

    def update_slot(self, item: AbstractItem = None, amount: int = 0):
        self.item = item
        self.amount = amount

    def add_amount(self, amount: int):
        self.update_slot(self.item, self.amount + amount)

    def can_place_in_slot(self, item: AbstractItem) -> bool:
        if self.allowed_types is None or item is None or item.ID == -1:
            return True
        return item.TYPE in self.allowed_types


class Inventory:
    def __init__(self, size: int):
        self.slots = []
        for slot in range(size):
            self.slots.append(InventorySlot(AbstractItem(-1, ""), 0))

    def clear(self):
        self.slots = []

    def empty_slot_count(self) -> int:
        counter = 0
        for slot in self.slots:
            if slot.item.ID == -1:
                counter += 1
        return counter

    def add_item(self, item: AbstractItem, amount: int) -> bool:
        if self.empty_slot_count() <= 0:
            return False

        slot = self.find_item_in_inv(item)

        if slot is None:
            self.set_empty_slot(item, amount)
            return True

        slot.add_amount(amount)
        return True

    def find_item_in_inv(self, item: AbstractItem):
        for slot in self.slots:
            if slot.item.ID == item.ID:
                return slot
        return None

    def set_empty_slot(self, item: AbstractItem, amount: int):
        for slot in self.slots:
            if slot.item.ID == -1:
                slot.update_slot(item, amount)
                return slot
        return None

    def remove_item(self, item: AbstractItem):
        for slot in self.slots:
            if slot.item == item:
                slot.update_slot()

    @staticmethod
    def swap_item(item1: InventorySlot, item2: InventorySlot):
        if item2.can_place_in_slot(item1.item) and item1.can_place_in_slot(item2.item):
            temp_slot = InventorySlot(item2.item, item2.amount)

            item2.update_slot(item1.item, item1.amount)
            item1.update_slot(temp_slot.item, temp_slot.amount)
