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

def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def _cal_angle(player1,player2):
    # 计算球员之间的夹角
    delta_x = player2.x - player1.x
    delta_y = player2.y - player1.y
    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)

    # 计算夹角差的绝对值
    angle_difference = abs(angle_degrees - player1.direction)
    return angle_difference


def _just_grab(player1,players):
    #判断是否能够直接获取球权
    #身边没有对方球员的情况
    collision_distance = 30
    for player in players:
        if get_distance(player1,player) < collision_distance:
            return False
    return True

def _how_to_grab(player1,blue_players):
    #判断以什么方向侧向踢出
    player_position = (player1['x'],player1['y'])
    # 定义球场划分的网格大小
    grid_length = 50
    grid_width = 50

    # 确定周围的空区域
    empty_regions = []
    for x in range(0, SCREEN_LENGTH, grid_length):
        for y in range(0, SCREEN_WIDTH, grid_width):
            region_center = (x + grid_length // 2, y + grid_width // 2)
            is_empty = all(math.sqrt((blue_player['x'] - region_center[0]) ** 2 + (blue_player['y'] - region_center[1]) ** 2) > 10 for blue_player in blue_players)
            if is_empty:
                empty_regions.append(region_center)

    # 计算方向
    kick_directions = []
    for region_center in empty_regions:
        direction_angle = math.atan2(region_center[1] - player_position[1], region_center[0] - player_position[0])
        direction_degree = math.degrees(direction_angle)
        kick_directions.append(direction_degree)
    return random.choice(kick_directions)