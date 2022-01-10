import random

# Общие
WIDTH = 1920
HEIGHT = 1080
BG = '#43485E'
BG_BTN = '#C8D1F7'
BG_BTN_SHADOW = '#242429'
# Игрок
PLAYER_SIZE = 40
STEP = 4
# Для вычисления координат
STEP_ANGLE = 1
MIN_COEFF = STEP_ANGLE // 60
MAX_COEFF = (MIN_COEFF * (360 // STEP_ANGLE))
# Генерация
N = random.randrange(20, 30, 2)
EMPTY_N = N // 2
CELL_SIZE = 180
MIN_ROAD = N // 10
MAX_ROAD = MIN_ROAD * 2
MASK = N // 5
RANGE_SQUARE = N // 2.5
