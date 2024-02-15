import math


def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    decisions.append({
        'type': 'move',
        'player_number': 0,
        'destination': ball,
        'direction':get_direction(blue_players[0],ball),
        'speed': 10,
    })
    
        
    return decisions



