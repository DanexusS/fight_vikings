"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


from sqlite3 import connect
from enums import Enum


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Attack_Radius = 2
    Damage = 3
    Health = 4
    Armor = 5
    Stamina = 6


class ItemType(Enum):
    Food = 0
    Equipment = 1
    Helmet = 2
    Chestplate = 3
    Pants = 4
    Boots = 5
    Weapon = 6
    Item = 7


class ItemBuff:
    def __init__(self, affected_attribute: Attributes, value: float):
        self.affected_attribute = affected_attribute
        self.value = value


class AbstractItem:
    def __init__(self, title: str = ""):
        self.ID = -1
        self.TYPE = ItemType.Item
        self.MAIN_TYPE = ItemType.Item
        self.title = title
        self.is_stackable = True
        self.image = None


class FoodItem(AbstractItem):
    def __init__(self, title: str):
        super().__init__(title)

        self.TYPE = ItemType.Food
        self.MAIN_TYPE = ItemType.Item

    def use_item(self):
        print(self.TYPE)


#   КЛАСС СНАРЯЖЕНИЯ
class EquipmentItem(AbstractItem):
    def __init__(self, title: str, durability: int, _type=None, buffs: list[ItemBuff] = None):
        super().__init__(title)

        self.TYPE = _type
        self.MAIN_TYPE = ItemType.Equipment
        self.buffs = buffs
        self.is_stackable = False
        self.durability = durability


#   КЛАСС ОРУЖИЯ
class WeaponItem(EquipmentItem):
    def __init__(self, title: str, durability: int, damage: int, buffs: list[ItemBuff] = None):
        super().__init__(title, durability, buffs=buffs)

        self.TYPE = ItemType.Weapon
        self.MAIN_TYPE = ItemType.Equipment
        self.damage = ItemBuff(Attributes.from_value(2), damage)


def is_equipment(_type):
    return _type == "Equipment" or _type == "Helmet" or \
           _type == "Chestplate" or _type == "Pants" or _type == "Boots"


def init():
    connection = connect("items_db.sqlite")
    cursor = connection.cursor()
    result = cursor.execute("""SELECT * FROM items""").fetchall()
    database = {}

    for elem in result:
        _type = elem[2]
        _title = elem[1]
        item = None

        if _type == "Food":
            item = FoodItem(_title)
            item.is_stackable = elem[3] == "True"
        elif is_equipment(_type):
            item = EquipmentItem(_title, durability=int(elem[6]), _type=ItemType.from_name(_type.lower()))
        elif _type == "Weapon":
            item = WeaponItem(_title, durability=int(elem[6]), damage=int(elem[7]))
        elif _type == "Item":
            item = AbstractItem(_title)
            item.TYPE = ItemType.Item
            item.is_stackable = elem[3] == "True"

        if _type == "Weapon" or is_equipment(_type):
            item.buffs = []
            if elem[5] != -1:
                for buff_id in map(int, str(elem[5]).split(";")):
                    buffs_db = cursor.execute(f"""SELECT * FROM buffs WHERE {int(buff_id)} = buffs.id""").fetchone()

                    if int(buffs_db[1]) > 0 and item.buffs is not None:
                        item.buffs.append(ItemBuff(Attributes.from_value(int(buffs_db[1]) - 1), float(buffs_db[2])))

        if item is not None:
            item.ID = elem[0]
            item.image = elem[4]
            database[_title] = item

    connection.close()
    return database
