import math
from utils import utils
import random

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))

def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

'''
def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    decisions.append({
        'type': 'grab',
        'player_number': 0,
    })
    return decisions
'''

def play(red_players, blue_players, ball, scoreboard):
    decisions = []  
    if ball['owner_color'] != 'blue':  # 对方球员持球时
        player_number = 4  # 对号入座，number为4的球员
        player = blue_players[player_number]
        distance = get_distance(player, ball)
        direction = get_direction(player,ball)
        decisions.append({
            'type':'collision',
            'player_number': player['number'],
            'direction': get_direction(player,ball),          
        })
        if distance >= 10:  
            decisions.append({
                'type': 'move',
                'player_number': player['number'],
                'destination': ball,
                'direction':direction,
                'speed': 10,
            })
        elif utils._just_grab(player,blue_players):
            decisions.append({
                'type': 'grab',
                'player_number': player['number'],
            })
        else:
            angle = utils._how_to_grab(player,blue_players)
            decisions.append({
                'type':'grab',
                'player_number':player['number'],
                'direction':angle,
            })

    else:
        maghsad = {'x': -300, 'y': 100}
        ball_owner = blue_players[ball['owner_number']]
        distance = get_distance(ball_owner, maghsad)
        direction = get_direction(ball_owner,maghsad)
        #print("现在蓝方持球")
        if distance >= 10:
            decisions.append({
                'type': 'move',
                'player_number': ball_owner['number'],
                'destination': maghsad,
                'direction':direction,
                'speed': 8,
            })
        else:
            hadaf = {'x': -500, 'y': 60}
            direction = get_direction(ball_owner, hadaf)
            decisions.append({
                'type': 'kick',
                'player_number': ball_owner['number'],
                'direction': direction,
                'power': 60,
            })
   
    return decisions