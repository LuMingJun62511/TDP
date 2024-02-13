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
def adjust_self():
    print('调整自己的位姿')
    return '调整自己的位姿'
def stand_still():
    print('站着不动')
    return '站着不动'
def chase_ball():
    print('追球')
    return '追球'

def pass_to_teammates():
    print('尽快传给队友')
    return '尽快传给队友'

# 根据上述代码，
def play(red_players, blue_players, ball, scoreboard):
    decisions = []

    if ball['x']>700:#球是否打入己方球门？
        serve_ball
    else: #球还没进
        if ball['x']>0:#球在我方半场？
            if ball['x']>200:#球进入禁区了？
                if ball['owner_number'] == 0 :  # 守门员是否已经成功拦截了球？
                    pass_to_teammates
                else:  # 还没拦截到，继续追球
                    chase_ball
            else: #球还没进入禁区
                adjust_self
        else:#球还不在我方半场
            stand_still


    # decisions.append({
    #     'type': 'move',
    #     'player_number': 0,
    #     'destination': ball,
    #     'speed': 10,
    # })

    return decisions




