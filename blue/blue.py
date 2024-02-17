import math
from utils import utils
import random
from roles import defender,goalkeeper,forward

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))

def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    ## if role is defender, move towards the ball
    for player in blue_players:
        if isinstance(player['role'], defender.Defender):
            print("defender",player['number'])
            decisions.append({
                'type': 'move',
                'player_number': player['number'],
                'destination': ball,
                'direction':get_direction(player,ball),
                'speed': 10,
            })
        elif isinstance(player['role'], forward.Forward):
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            # Placeholder for forward decision logic
            pass
        else:
            print(f"Unrecognized player role for player {player['number']}")
            
    return decisions