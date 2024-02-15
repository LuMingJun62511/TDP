import math
import utils
import random

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

def get_strategic_point():
    return 

def check_pass_feasibility():
    return

def pass_ball_to_forward():
    return

def plan_path_for_pass():
    return

def is_at_strategic_point():
    return

def adjust_self():
    return

def move_to_strategic_point():
    return

def is_closer_to_ball():
    return 

def intercept_the_ball():
    return 



#  ball的一个实例 {'x': -211, 'y': 256, 'radius': 8, 'owner_color': 'red', 'owner_number': 3, 'direction': 2.2865803711201833, 'speed': 0}
# red_players的一个实例[{'x': -330, 'y': 0, 'name': 'Player0', 'number': 0, 'radius': 24, 'ban_cycles': 0}, {'x': -326, 'y': 110, 'name': 'Player1', 'number': 1, 'radius': 16, 'ban_cycles': 0}, {'x': -226, 'y': -200, 'name': 'Player2', 'number': 2, 'radius': 16, 'ban_cycles': 0}, {'x': -151, 'y': 200, 'name': 'Player3', 'number': 3, 'radius': 16, 'ban_cycles': 0}, {'x': -75, 'y': -200, 'name': 'Player4', 'number': 4, 'radius': 16, 'ban_cycles': 0}, {'x': 0, 'y': 200, 'name': 'Player5', 'number': 5, 'radius': 16, 'ban_cycles': 0}]
# red_players的一个实例[{'x': 270, 'y': 0, 'name': 'Player0', 'number': 0, 'radius': 24, 'ban_cycles': 0}, {'x': 302, 'y': -200, 'name': 'Player1', 'number': 1, 'radius': 16, 'ban_cycles': 0}, {'x': 226, 'y': 200, 'name': 'Player2', 'number': 2, 'radius': 16, 'ban_cycles': 0}, {'x': 151, 'y': -200, 'name': 'Player3', 'number': 3, 'radius': 16, 'ban_cycles': 0}, {'x': 39, 'y': 184, 'name': 'Player4', 'number': 4, 'radius': 16, 'ban_cycles': 0}, {'x': 0, 'y': -200, 'name': 'Player5', 'number': 5, 'radius': 16, 'ban_cycles': 0}]
def play(red_players, blue_players, ball, scoreboard):
    decisions = []

    if ball['x'] < 0:  # Is the ball on our half of the field?
        if ball['owner_color'] == 'red': #我方持球？
            if ball['owner_color'] == 1:#本人持球？
                if check_pass_feasibility():#适合传球？
                    pass_ball_to_forward()
                else:
                    plan_path_for_pass()
            else:
                if is_at_strategic_point():
                    adjust_self()
                else:
                    move_to_strategic_point()

        else:
            if is_closer_to_ball():
                intercept_the_ball()
            else:
                move_to_strategic_point()

    else:
        if is_at_strategic_point():
            adjust_self()
        else:
            move_to_strategic_point()



    return decisions

