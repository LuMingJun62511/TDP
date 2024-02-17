import pygame as pg
import math
from .size import *
import random

def convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y):
    pygame_x = SCREEN_LENGTH // 2 + cartesian_x
    pygame_y = SCREEN_WIDTH // 2 - cartesian_y
    return pygame_x, pygame_y


def write_text_on_pygame_screen(screen, font_size, color, text, cartesian_x, cartesian_y, font=None):
    pygame_x, pygame_y = convert_coordinate_cartesian_to_pygame(cartesian_x, cartesian_y)
    font = pg.font.Font(font, font_size)
    text_render = font.render(text, True, color)
    screen.blit(text_render, (pygame_x, pygame_y))


#以下的代码考虑到复用性，所以暂时写在 utils，后续可以更改
def distance(cartesian_p1, cartesian_p2):
    return ((cartesian_p1.x - cartesian_p2.x) ** 2 + (cartesian_p1.y - cartesian_p2.y) ** 2) ** 0.5

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

