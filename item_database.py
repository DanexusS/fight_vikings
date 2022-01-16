import sqlite3
from items import *
from constants import Attributes


def init():
    con = sqlite3.connect("items_db.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT * FROM items""").fetchall()
    db = {}

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
                    buffs_db = cur.execute(f"""SELECT * FROM buffs WHERE {int(buff_id)} = buffs.id""").fetchone()

                    if int(buffs_db[1]) > 0 and item.buffs is not None:
                        item.buffs.append(ItemBuff(Attributes.from_value(int(buffs_db[1]) - 1), float(buffs_db[2])))

        if item is not None:
            item.ID = elem[0]
            item.image = elem[4]
            db[_title] = item

    con.close()
    return db
