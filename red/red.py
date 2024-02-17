import math
from roles import goalkeeper,defender,forward

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    goal_position = {'x': 500, 'y': 0}  # Example goal position for scoring

    for player in red_players:
        print('player:',player)
        print(f"Role type: {type(player['role'])}")
        if isinstance(player['role'], goalkeeper.GoalKeeper):
            print(f"Player {player['number']} is a goalkeeper.")
            
    return decisions


