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

def adjust_self(players, ball, GOALKEEPER_WIDTH, GOALKEEPER_DEPTH):
    goalkeeper = players[0]  # ゴールキーパーの情報
    goal_center = {'x': -460, 'y': 0}  # ゴールの中心

    # 楕円の半径
    a = GOALKEEPER_DEPTH / 2
    b = GOALKEEPER_WIDTH / 2

    # ボールとゴールの中心とを結ぶ直線の傾きと切片を計算
    if ball['x'] != goal_center['x']:
        slope = (ball['y'] - goal_center['y']) / (ball['x'] - goal_center['x'])
        intercept = goal_center['y'] - slope * goal_center['x']
    else:
        slope = None

    # 楕円と直線の交点を計算
    if slope is not None:
        # 楕円の方程式と直線の方程式を組み合わせて交点を求める
        # y = mx + b を楕円の方程式に代入して解く
        A = (1 + slope**2 / b**2)
        B = 2 * slope * intercept / b**2
        C = (intercept / b)**2 - 1
        # 二次方程式 Ax^2 + Bx + C = 0 の解
        delta = B**2 - 4 * A * C
        if delta >= 0:
            x1 = (-B + math.sqrt(delta)) / (2 * A)
            x2 = (-B - math.sqrt(delta)) / (2 * A)
            # 2つの解のうち、ボールに近い方を選択
            x_target = x1 if abs(x1 - ball['x']) < abs(x2 - ball['x']) else x2
            y_target = slope * x_target + intercept
        else:
            # 実際にはここに到達することはありませんが、計算上のエラーに備えてゴール中心をターゲットとします。
            x_target = goal_center['x']
            y_target = goal_center['y']
    else:
        # 傾きが無限大の場合（縦の直線）
        x_target = goal_center['x']
        y_target = ball['y']
        if abs(y_target) > b:  # 楕円の範囲外の場合は、範囲内に修正
            y_target = b * (y_target / abs(y_target))

    return {
        'type': 'move',
        'player_number': goalkeeper['number'],
        'destination': {'x': x_target, 'y': y_target},
        'speed': 10
    }
    
    
    
    

def stand_still():
    print('站着不动')
    return '站着不动'
def chase_ball():
    print('追球')
    return '追球'

def pass_to_teammates():
    print('尽快传给队友')
    return '尽快传给队友'

# Based on the above code,
def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    if ball['x'] < -460:  # Has the ball entered our goal?
        serve_ball()  # Can trigger
    else:  # The ball hasn't entered the goal
        if ball['x'] < 0:  # Is the ball on our half of the field?
            if ball['x'] < -300:  # Has the ball entered the penalty area?
                if ball['owner_number'] == 0:  # Has the goalkeeper successfully intercepted the ball?
                    pass_to_teammates()  # Can trigger
                else:  # Not intercepted yet, continue to chase the ball
                    chase_ball()  # Can trigger
            else:  # The ball has not entered the penalty area
                decision = adjust_self(red_players, ball, 160, 210)  
                decisions.append(decision)
        else:  # The ball is not on our half of the field
            stand_still()  # Can trigger

    decisions.append({
        'type': 'move',
        'player_number': 0,
        'destination': ball,
        'speed': 10,
    })

    return decisions



