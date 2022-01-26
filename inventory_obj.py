"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


from item_database import AbstractItem


class InventorySlot:
    def __init__(self, item, amount: int, before_update=None, after_update=None,
                 allowed_types=None):
        self.item = item
        self.amount = amount
        self.allowed_types = allowed_types if allowed_types else []
        self.ui_display = item.image
        self.mouse_hovered = False
        self.before_update = before_update if before_update else []
        self.after_update = after_update if after_update else []

    def save_data(self):
        fieldnames = ["item", "amount"]
        data = [self.item.title, self.amount]
        info = {}

        for i in range(len(data)):
            info[fieldnames[i]] = data[i]
        return info

    def update_slot(self, item=None, amount: int = 0):
        if self.before_update:
            for func in self.before_update:
                if func:
                    func(self, -1)

        self.item = item
        self.amount = amount
        self.ui_display = item.image

        if self.before_update:
            for func in self.before_update:
                if func:
                    func(self)

    def add_amount(self, amount: int):
        self.update_slot(self.item, self.amount + amount)

    def can_place_in_slot(self, item) -> bool:
        if self.allowed_types == [] or item is None or item.ID == -1:
            return True
        return item.TYPE in self.allowed_types


class Inventory:
    def __init__(self, size: int, num_of_rows: int, default_items=None):
        height = size // num_of_rows
        width = size // height

        self.slots = [[InventorySlot(AbstractItem(), 0) for __ in range(width)]
                      for _ in range(height)]

        if default_items:
            for item in default_items:
                self.add_item(item)

        self.interface = None

    def set_slot(self, row, column, slot):
        self.slots[row][column] = slot

    def empty_slot_count(self) -> int:
        counter = 0
        for row in self.slots:
            for slot in row:
                if slot.item.ID == -1:
                    counter += 1
        return counter

    def add_item(self, item, amount: int = 1) -> bool:
        if self.empty_slot_count() <= 0:
            return False

        slot = self.find_item_in_inv(item)

        if not item.is_stackable or slot is None:
            self.set_empty_slot(item, amount)
            return True

        slot.add_amount(amount)
        return True

    def find_item_in_inv(self, item):
        for row in self.slots:
            for slot in row:
                if slot.item.ID == item.ID:
                    return slot
        return None

    def set_empty_slot(self, item, amount: int):
        for row in self.slots:
            for slot in row:
                if slot.item.ID == -1:
                    slot.update_slot(item, amount)
                    return slot
        return None

    def remove_item(self, item):
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
