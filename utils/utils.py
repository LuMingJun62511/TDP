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
    x = p2['x']- p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x'] ) ** 2 + (p1['y'] - p2['y'] ) ** 2) ** 0.5)

def cal_angle(player1, player2):
    delta_x = player2['x'] - player1['x']
    delta_y = player2['y'] - player1['y']
    # delta_x = player2.x - player1.x
    # delta_y = player2.y - player1.y
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees


def just_grab(player1,players):
    for player in players:
        if get_distance(player1,player) < 20:
            return False
    return True

def how_to_grab(player1,players):
    # player_position = (player1.x,player1.y)
    player_position = (player1['x'],player1['y'])
    # 定义球场划分的网格大小
    grid_width = 50
    grid_height = 50
    # 确定周围的空区域
    empty_regions = []
    for x in range(0, SCREEN_LENGTH, grid_width):
        for y in range(0, SCREEN_WIDTH, grid_height):
            region_center = (x + grid_width // 2, y + grid_height // 2)
            is_empty = all(math.sqrt((player['x'] - region_center[0]) ** 2 + (player['y'] - region_center[1]) ** 2) > PLAYER_RADIUS for player in players)
            # is_empty = all(math.sqrt((player.x - region_center[0]) ** 2 + (player.y - region_center[1]) ** 2) > PLAYER_RADIUS for player in players)
            if is_empty:
                empty_regions.append(region_center)

    # 计算方向
    kick_directions = []
    for region_center in empty_regions:
        direction_angle = math.atan2(region_center[1] - player_position[1], region_center[0] - player_position[0])
        direction_degree = math.degrees(direction_angle)
        kick_directions.append(direction_degree)
    if kick_directions:
        random_direction = random.choice(kick_directions)
        return random_direction
    else:
        print("没有可用的方向")
