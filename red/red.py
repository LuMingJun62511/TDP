import math
from roles.goalkeeper import GoalKeeper
from roles.defender import Defender
from roles.forward import Forward
from utils import utils
from models import Player
# Assuming the existence of utility functions get_direction and get_distance
# These functions compute the direction and distance between two points

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

def play(red_players, blue_players, ball, scoreboard):
    decisions = []  
    if ball['owner_color'] != 'red':
        closest_player = red_players[1]
        for player in red_players:
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
                'speed': 8,
            })
        elif utils._just_grab(closest_player,blue_players):
            decisions.append({
                'type': 'grab',
                'player_number': closest_player['number'],
            })
        else:
            angle = utils._how_to_grab(closest_player,blue_players)
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
    goal_position = {'x': 500, 'y': 0}  # Example goal position for scoring
    # Loop through each player in the red team
    for player in red_players:
        own_half = (-450,0)
        strategic_position = {'x':-200,'y':100}
        # Depending on the role, call the appropriate decision-making function
        #if isinstance(player['role'], goalkeeper.GoalKeeper):
        if player['role'] == 'goalkeeper':
            #print('player is goalkeeper')
            goalkeeper = GoalKeeper(color='red',**player)
            decisions.extend(goalkeeper.decide_action(ball, red_players))
        #elif isinstance(player['role'], defender.Defender):
        elif player['role'] == 'defender':
            # Defenders make decisions based on ball possession and strategic positioning
            #print('player is defender')
            defender = Defender(color='red',**player)
            decisions.extend(defender.decide_action(ball, red_players,own_half, strategic_position))
        #elif isinstance(player['role'], forward.Forward):
        elif player['role'] == 'forward':
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            # Placeholder for forward decision logic
            pass
        else:
            print(f"Unrecognized player role for player {player['number']}")

    return decisions


