from .size import *
from .utils import *
from models import player

PLAYER_COUNT = 5

FRICTION = main_size // 2 #5
MAX_PLAYER_SPEED = PLAYER_RADIUS
MAX_KICK_POWER = make_even_number(main_size * 6) # 60


# RULES
ALLOWED_PLAYERS_IN_PENALTY_AREA_NUMBER = 4
ALLOWED_PLAYERS_AROUND_BALL_NUMBER = 2
ALLOWED_PLAYERS_AROUND_BALL_RADIUS = make_even_number(3 * (PLAYER_RADIUS + BALL_RADIUS))  # 54
BALL_CROWDED_BAN_CYCLES = 25
PENALTY_ARIA_BAN_CYCLES = 20


RED_PLAYERS_INITIAL_VALUES = []
BLUE_PLAYERS_INITIAL_VALUES = []


RED_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': -FOOTBALL_PITCH_LENGTH // 2 + 3 * GOAL_DEPTH,
    'y': 0,
    'name': "Player{}".format(0),
    'radius': PLAYER_RADIUS + BALL_RADIUS,
    'role':'goalkeeper'
})

BLUE_PLAYERS_INITIAL_VALUES.append({
    'number': 0,
    'x': FOOTBALL_PITCH_LENGTH // 2 - 3 * GOAL_DEPTH,
    'y': 0,
    'name': "Player{}".format(0),
    'radius': PLAYER_RADIUS + BALL_RADIUS,
    'role':'goalkeeper'
})

'''
number = 0
color_red = 'red'
color_blue = 'blue'
x = -FOOTBALL_PITCH_WIDTH // 2 + 3 * GOAL_DEPTH
y = 0
name = "Player{}".format(0)
radius = PLAYER_RADIUS + BALL_RADIUS
role = 'goalkeeper'
RED_PLAYERS_INITIAL_VALUES.append({
    player.Player(x,y,name,number,color_red,radius,role)
})

BLUE_PLAYERS_INITIAL_VALUES.append({
    player.Player(-x,y,name,number,color_blue,radius,role)
})
'''

for i in range(1, PLAYER_COUNT):
    x = (FOOTBALL_PITCH_LENGTH // 2 // (PLAYER_COUNT // 2) + 1) * (PLAYER_COUNT - i - 1) // 2
    y = FOOTBALL_PITCH_WIDTH // 3 if i % 2 == 1 else -FOOTBALL_PITCH_WIDTH // 3
    RED_PLAYERS_INITIAL_VALUES.append({
        'number': i,
        'x':-x,
        'y': y,
        'name': "Player{}".format(i),
        'radius': PLAYER_RADIUS,
        'role':'defender'
    })
    BLUE_PLAYERS_INITIAL_VALUES.append({
        'number': i,
        'x': x,
        'y': -y,
        'name': "Player{}".format(i),
        'radius': PLAYER_RADIUS,
        'role':'defender'
    })
'''

for i in range(1, PLAYER_COUNT):
    x = (FOOTBALL_PITCH_WIDTH // 2 // (PLAYER_COUNT // 2) + 1) * (PLAYER_COUNT-i-1) // 2
    y = FOOTBALL_PITCH_HEIGHT // 3 if i % 2 == 1 else -FOOTBALL_PITCH_HEIGHT // 3
    number = i
    name = "Player{}".format(i)
    radius = PLAYER_RADIUS
    RED_PLAYERS_INITIAL_VALUES.append({
        player.Player(x,y,name,number,color_red,radius)
    })
    BLUE_PLAYERS_INITIAL_VALUES.append({
        player.Player(x,y,name,number,color_blue,radius)
    })
'''
SHOULD_PRINT_DECISIONS_ERROR = True
