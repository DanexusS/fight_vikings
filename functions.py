import pygame
import os


def load_image(name):
    fullname = os.path.join('images/', name)
    return pygame.image.load(fullname).convert_alpha()