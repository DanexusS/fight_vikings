import os
from constants import *


def load_image(name):
    fullname = os.path.join('images/', name)
    return pygame.image.load(fullname).convert_alpha()


def size_img(name, num=1):
    return pygame.transform.scale(load_image(name), (CELL_SIZE * num, CELL_SIZE * num))
