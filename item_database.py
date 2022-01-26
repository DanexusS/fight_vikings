"""
    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        Fight Vikings
                         ver. 1.0.0
      ©2021-2022. Dunk Corporation. All rights reserved

    -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""


from sqlite3 import connect
from items import *


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
        elif _type == "Equipment":
            item = EquipmentItem(_title, durability=int(elem[6]))
        elif _type == "Weapon":
            item = WeaponItem(_title, durability=int(elem[6]), damage=int(elem[7]))
        elif _type == "Item":
            item = AbstractItem(_title)
            item.TYPE = ItemType.Item
            item.is_stackable = elem[3] == "True"

        if _type == "Weapon" or _type == "Equipment":
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
