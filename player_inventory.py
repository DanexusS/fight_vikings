import csv
from enums import Enum


class Attributes(Enum):
    Move_Speed = 0
    Attack_Speed = 1
    Attack_Radius = 2
    Damage = 3
    Health = 4
    Armor = 5
    Stamina = 6


class PlayerAttributes:
    def __init__(self):
        attributes = Attributes.as_dict()

        csv_file = open("hero_stats.csv", encoding="utf8", newline="")
        reader = list(csv.DictReader(csv_file, fieldnames=["name", "value"], delimiter=";"))[1:]

        for row in reader:
            attributes[row["name"].lower()] = float(row["value"])
