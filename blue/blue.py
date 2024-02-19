import math
from utils import utils
import random
from utils import SCREEN_LENGTH,SCREEN_WIDTH
from roles.goalkeeper import GoalKeeper
from roles.defender import Defender
from roles.forward import Forward

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))

def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    own_half = (-450,0)
    strategic_position = {'x':-200,'y':100}
    
    ## if role is defender, move towards the ball
    for player in blue_players:
        field_map_blue = {
            'goal': {'x': -450, 'y': 0},  # 例如，这里是球门的位置
            'opponent_goal': {'x': 450, 'y': 0},  # 对手的球门位置
            'width': SCREEN_LENGTH,  # 球场宽度
            'height': SCREEN_WIDTH,  # 球场高度
            'cost': [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # 成本地图，用于A*算法
        }
        if player['role'] == 'goalkeeper':

        # Depending on the role, call the appropriate decision-making function
        #if isinstance(player['role'], goalkeeper.GoalKeeper):
            goalkeeper = GoalKeeper(color='blue',**player)
            decisions.extend(goalkeeper.decide_action(ball, blue_players))
        elif player['role'] == 'defender':
            # Defenders make decisions based on ball possession and strategic positioning
            #print('player is defender')
            defender = Defender(color='blue',**player)
            decisions.extend(defender.decide_action(ball, blue_players))
    
        #elif isinstance(player['role'], forward.Forward):
        elif player['role'] == 'forward':
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            # Placeholder for forward decision logic
            forward = Forward(color='blue',**player)
            decisions.extend(forward.decide_action(ball, blue_players,red_players,field_map_blue))
        else:
            print(f"Unrecognized player role for player {player['number']}")

    return decisions