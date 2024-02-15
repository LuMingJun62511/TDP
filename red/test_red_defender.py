import math
import utils
import random

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)

# 好的，还是先实现决策树
def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    # if 碰撞检测逻辑:
    #     decisions.append({
    #         'type':'collision',
    #         'player_number': closest_player['number'],
    #         'direction': get_direction(closest_player,ball),          
    #     })

    # if ball['x'] < 0:  # Is the ball on our half of the field?
    #     if ball['owner_color'] == 'red': #我方持球？
    #         if 本人持球？:
    #             if 适合传球？:
    #                 pass_ball_to_forward()
    #             else:
    #                 plan_to_pass()
    #         else:
    #             if check_at_strategic_point():
    #                 adjust_self()
    #             else:
    #                 move_to_strategic_point()

    #     else:
    #         if closer_to_ball():
    #             intercept_the_ball()
    #         else:
    #             move_to_strategic_point()

    # else:
    #     if check_at_strategic_point():
    #         adjust_self()
    #     else:
    #         move_to_strategic_point()




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

