from items import *


class InventorySlot:
    def __init__(self, item: AbstractItem, amount: int, allowed_types: list[ItemType] = None):
        if allowed_types is None:
            allowed_types = []

        self.item = item
        self.amount = amount
        self.allowed_types = allowed_types
        self.ui_display = item.image
        self.parent = None
        self.mouse_hovered = False

    def update_slot(self, item: AbstractItem = None, amount: int = 0):
        self.item = item
        self.amount = amount
        self.ui_display = item.image

    def add_amount(self, amount: int):
        self.update_slot(self.item, self.amount + amount)

    def can_place_in_slot(self, item: AbstractItem) -> bool:
        if self.allowed_types == [] or item is None or item.ID == -1:
            return True
        return item.TYPE in self.allowed_types


class Inventory:
    def __init__(self, size: int, num_of_rows: int, default_items: list[AbstractItem] = None):
        height = size // num_of_rows
        width = size // height

        self.slots = [[InventorySlot(AbstractItem(), 0) for __ in range(width)]
                      for _ in range(height)]

        if default_items is not None:
            for item in default_items:
                self.add_item(item)

    def clear(self):
        self.slots = []

    def empty_slot_count(self) -> int:
        counter = 0
        for row in self.slots:
            for slot in row:
                if slot.item.ID == -1:
                    counter += 1
        return counter

    def add_item(self, item: AbstractItem, amount: int = 1) -> bool:
        if self.empty_slot_count() <= 0:
            return False

        slot = self.find_item_in_inv(item)

        if not item.is_stackable or slot is None:
            self.set_empty_slot(item, amount)
            return True

        slot.add_amount(amount)
        return True

    def find_item_in_inv(self, item: AbstractItem):
        for row in self.slots:
            for slot in row:
                if slot.item.ID == item.ID:
                    return slot
        return None

    def set_empty_slot(self, item: AbstractItem, amount: int):
        for row in self.slots:
            for slot in row:
                if slot.item.ID == -1:
                    slot.update_slot(item, amount)
                    return slot
        return None

    def remove_item(self, item: AbstractItem):
        for row in self.slots:
            for slot in row:
                if slot.item == item:
                    slot.update_slot()

    @staticmethod
    def swap_item(slot1: InventorySlot, slot2: InventorySlot):
        if slot2.can_place_in_slot(slot1.item) and slot1.can_place_in_slot(slot2.item):
            temp_slot = InventorySlot(slot2.item, slot2.amount)

            slot2.update_slot(slot1.item, slot1.amount)
            slot1.update_slot(temp_slot.item, temp_slot.amount)
