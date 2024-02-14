import math

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def serve_ball():
    print('捡球')
    return '捡球'

def adjust_self(player, ball, GOALKEEPER_WIDTRH, GOALKEEPER_DEPTH):
    goalkeeper = player[0]
    # 楕円形の範囲を定義
    ellipse_width = GOALKEEPER_WIDTRH
    ellipse_height = GOALKEEPER_DEPTH
    goal_x, goal_y = -460, 0

    # プレイヤーとボールの位置
    player_x, player_y = goalkeeper['x'], goalkeeper['y']
    ball_x, ball_y = ball['x'], ball['y']

    # ゴールとボールの間の距離
    distance_to_ball = get_distance({'x': goal_x, 'y': goal_y}, ball)
    print('ゴールとボールの間の距離', distance_to_ball)

    # ゴールからボールへの方向
    angle_to_ball = math.atan2(ball_y - goal_y, ball_x - goal_x)
    print('プレイヤーとボールの間の距離', get_distance({'x': player_x, 'y': player_y}, ball))

    # 楕円形の境界上の点を計算
    ellipse_x = goal_x + (ellipse_width / 2) * math.cos(angle_to_ball)
    ellipse_y = goal_y + (ellipse_height / 2) * math.sin(angle_to_ball)
    print('楕円形の境界上の点', ellipse_x, ellipse_y)

    # プレイヤーの位置を調整
    if distance_to_ball > get_distance({'x': ellipse_x, 'y': ellipse_y}, {'x': goal_x, 'y': goal_y}):
        # 楕円形の境界上に移動
        new_x = ellipse_x
        new_y = ellipse_y
    else:
        # 現在位置が適切な場合は移動しない
        new_x = player_x
        new_y = player_y
    
    print('調整', new_x, new_y)
    
    return {
        'type': 'move',
        'player_number': 0,
        'destination': {'x': new_x, 'y': new_y},
        'speed': 10
    }
    

def stand_still():
    print('站着不动')
    return '站着不动'
def chase_ball():
    print('追球')
    return '追球'

def pass_to_teammates():
    print('传球')
    return '传球'

# Based on the above code,
def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    if ball['x'] < -460:  # Has the ball entered our goal?
        serve_ball()  # Can trigger
    else:  # The ball hasn't entered the goal
        if ball['x'] < 0:  # Is the ball on our half of the field?
            print('ball', ball)
            if ball['x'] < -300:  # Has the ball entered the penalty area?
                if ball['owner_number'] == 0:  # Has the goalkeeper successfully intercepted the ball?
                    pass_to_teammates()  # Can trigger
                else:  # Not intercepted yet, continue to chase the ball
                    chase_ball()  # Can trigger
                    decisions.append({
                        'type': 'move',
                        'player_number': 0,
                        'destination': ball,
                        'speed': 10,
                    })
            else:  # The ball is on our half of the field, but not in the penalty area
                if ball['owner_number'] == 0:  # Has the goalkeeper successfully intercepted the ball?
                    pass_to_teammates()  # Can trigger
                decision = adjust_self(red_players, ball, 160, 210)  
                decisions.append(decision)
        else:  # The ball is not on our half of the field
            stand_still()  # Can trigger

    return decisions



