class Attributes:
    Move_Speed = 0
    Attack_Speed = 1
    Damage = 2
    # потом дополнить


class ItemType:
    Null = -1
    Food = 0
    Equipment = 1
    Weapon = 2
    Potion = 3
    Item = 4


class ItemBuff:
    def __init__(self, affected_attribute: Attributes, value: int):
        self.affected_attribute = affected_attribute
        self.value = value


class AbstractItem:
    def __init__(self, title: str = ""):
        self.ID = -1
        self.TYPE = ItemType.Null
        self.title = title
        self.is_stackable = True
        self.image = None


class AbstractUsingItem(AbstractItem):
    def __init__(self, title: str, use_key):
        super().__init__(title)

        self.use_key = use_key

    def use_item(self):
        pass


#   КЛАСС СНАРЯЖЕНИЯ
class EquipmentItem(AbstractItem):
    def __init__(self, item_type: ItemType, title: str, durability: int, buffs: list[ItemBuff] = None):
        super().__init__(title)

        self.TYPE = item_type
        self.buffs = buffs
        self.is_stackable = False
        self.durability = durability


#   КЛАСС ЕДЫ
class FoodItem(AbstractUsingItem):
    def __init__(self, title: str, use_key):
        super().__init__(title, use_key)

        self.TYPE = ItemType.Food

    def use_item(self):
        print("used item food")
