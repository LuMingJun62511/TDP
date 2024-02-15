import math
import utils
import random

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

def _just_grab(player1,players):
    collision_distance = 30
    for player in players:
        if get_distance(player1,player) < collision_distance:
            return False
    return True

def _how_to_grab(player1,blue_players):
    player_position = (player1['x'],player1['y'])
    # 定义球场划分的网格大小
    grid_length = 50
    grid_width = 50

    # 确定周围的空区域
    empty_regions = []
    for x in range(0, utils.SCREEN_LENGTH, grid_length):
        for y in range(0, utils.SCREEN_WIDTH, grid_width):
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


def play(red_players, blue_players, ball, scoreboard):

    print('看看看看看看看看看看')
    print(red_players)
    print(blue_players)
    print('劈劈劈劈劈')

    decisions = []
    if ball['owner_color'] != 'red':
        closest_player = red_players[1]
        for player in red_players[2:]:
            if get_distance(player, ball) < get_distance(closest_player, ball):
                closest_player = player
        decisions.append({
            'type':'collision',
            'player_number': closest_player['number'],
            'direction': get_direction(closest_player,ball),          
        })
        if get_distance(closest_player, ball) >= 10:
            decisions.append({
                'type': 'move',
                'player_number': closest_player['number'],
                'destination': ball,
                'direction': get_direction(closest_player,ball),
                'speed': 10,
            })
        elif _just_grab(closest_player,blue_players):
            decisions.append({
                'type': 'grab',
                'player_number': closest_player['number'],
            })
        else:
            angle = _how_to_grab(closest_player,blue_players)
            decisions.append({
                'type':'grab',
                'player_number':closest_player['number'],
                'direction':angle,
            })
    else:
        maghsad = {'x': 300, 'y': -100}
        ball_owner = red_players[ball['owner_number']]
        distance = get_distance(ball_owner, maghsad)
        if distance >= 10:
            #print("现在红方持球")
            decisions.append({
                'type': 'move',
                'player_number': ball_owner['number'],
                'destination': maghsad,
                'direction':get_direction(ball_owner,maghsad),
                'speed': 8,
            })
            
        else:
            hadaf = {'x': 500, 'y': -60}
            direction = get_direction(ball_owner, hadaf)
            decisions.append({
                'type': 'kick',
                'player_number': ball_owner['number'],
                'direction': direction,
                'power': 60,
            })

    return decisions



