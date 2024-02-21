import math
from roles.goalkeeper import GoalKeeper
from roles.defender import Defender
from roles.forward import Forward
from utils import SCREEN_LENGTH,SCREEN_WIDTH
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
    # Loop through each player in the red team
    for player in red_players:
        # Depending on the role, call the appropriate decision-making function
        if player['role'] == 'goalkeeper':
            #print('player is goalkeeper')
            goalkeeper = GoalKeeper(color='red',**player)
            decisions.extend(goalkeeper.decide_action(ball, red_players))
        elif player['role'] == 'defender':
            # Defenders make decisions based on ball possession and strategic positioning
            #print('player is defender')
            defender = Defender(color='red',**player)
            decisions.extend(defender.decide_action(ball, red_players))
    
        elif player['role'] == 'forward':
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            # Placeholder for forward decision logic
            forwrad = Forward(color='red',**player)
            decisions.extend(forwrad.decide_action(ball, red_players,blue_players))           
        else:
            print(f"Unrecognized player role for player {player['number']}")

    return decisions


