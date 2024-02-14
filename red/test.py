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

    # ゴールからボールへの方向
    angle_to_ball = math.atan2(ball_y - goal_y, ball_x - goal_x)

    # 楕円形の境界上の点を計算
    ellipse_x = goal_x + (ellipse_width / 2) * math.cos(angle_to_ball)
    ellipse_y = goal_y + (ellipse_height / 2) * math.sin(angle_to_ball)

    # プレイヤーの位置を調整
    if distance_to_ball > get_distance({'x': ellipse_x, 'y': ellipse_y}, {'x': goal_x, 'y': goal_y}):
        # 楕円形の境界上に移動
        new_x = ellipse_x
        new_y = ellipse_y
    else:
        # 現在位置が適切な場合は移動しない
        new_x = player_x
        new_y = player_y
    
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

def pass_to_teammates(players, ball):
    print('パス出す')
    decisions = []
    goalkeeper_number = 0  # ゴールキーパーの番号を定義

    # ゴールキーパーの位置を取得
    goalkeeper_position = next(player for player in players if player['number'] == goalkeeper_number)

    # ゴールキーパー以外のチームメイトを選択
    teammates = [player for player in players if player['number'] != goalkeeper_number]

    # チームメイトがいない場合、何もしない
    if not teammates:
        return decisions

    # 最適なチームメイトを選択するロジック（ここでは単純に最も近いチームメイトを選択）
    closest_teammate = min(teammates, key=lambda player: get_distance(player, ball))

    # パスの方向を計算
    pass_direction = get_direction(goalkeeper_position, closest_teammate)

    # パスのパワーを決定（ここでは一定値を使用。状況に応じて調整が必要）
    pass_power = 50  # 適宜調整

    # パスの決定を追加
    return {
        'type': 'kick',
        'player_number': goalkeeper_number,
        'direction': pass_direction,
        'power': pass_power,
    }



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
                    decision = pass_to_teammates(red_players, ball)
                    decisions.append(decision)
                else:
                    chase_ball()  # Can trigger
                    decisions.append({
                        'type': 'move',
                        'player_number': 0,
                        'destination': ball,
                        'speed': 10,
                    })
            else:  # The ball is on our half of the field, but not in the penalty area
                decision = adjust_self(red_players, ball, 160, 210)  
                decisions.append(decision)
        else:  # The ball is not on our half of the field
            stand_still()  # Can trigger

    return decisions



