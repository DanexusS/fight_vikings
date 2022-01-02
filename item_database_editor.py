import sqlite3
from items import *


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
            item = EquipmentItem(_title, int(elem[5]))
        elif _type == "Weapon":
            item = WeaponItem(_title, int(elem[5]), int(elem[7]))
        elif _type == "Item":
            item = AbstractItem(_title)
            item.is_stackable = elem[3] == "True"

        if item is not None:
            item.ID = elem[0]
            item.image = elem[4]
            db[_title] = item

    con.close()
    return db
