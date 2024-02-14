import math

def get_direction(p1, p2):
    x = p2['x'] - p1['x']
    y = p2['y'] - p1['y']
    return math.degrees(math.atan2(y, x))


def get_distance(p1, p2):
    return int(((p1['x'] - p2['x']) ** 2 + (p1['y'] - p2['y']) ** 2) ** 0.5)


def serve_ball():
    print('Pick up the ball')
    return 'Pick up the ball'

def adjust_self(player, ball, GOALKEEPER_WIDTH, GOALKEEPER_DEPTH):
    goalkeeper = player[0]
    # Define the range of the ellipse
    ellipse_width = GOALKEEPER_WIDTH
    ellipse_height = GOALKEEPER_DEPTH
    goal_x, goal_y = -460, 0

    # Positions of the player and the ball
    player_x, player_y = goalkeeper['x'], goalkeeper['y']
    ball_x, ball_y = ball['x'], ball['y']

    # Distance between the goal and the ball
    distance_to_ball = get_distance({'x': goal_x, 'y': goal_y}, ball)

    # Direction from the goal to the ball
    angle_to_ball = math.atan2(ball_y - goal_y, ball_x - goal_x)

    # Calculate the point on the boundary of the ellipse
    ellipse_x = goal_x + (ellipse_width / 2) * math.cos(angle_to_ball)
    ellipse_y = goal_y + (ellipse_height / 2) * math.sin(angle_to_ball)

    # Adjust the position of the player
    if distance_to_ball > get_distance({'x': ellipse_x, 'y': ellipse_y}, {'x': goal_x, 'y': goal_y}):
        # Move to the boundary of the ellipse
        new_x = ellipse_x
        new_y = ellipse_y
    else:
        # Do not move if the current position is appropriate
        new_x = player_x
        new_y = player_y
    
    return {
        'type': 'move',
        'player_number': 0,
        'destination': {'x': new_x, 'y': new_y},
        'speed': 10
    }
    

def stand_still():
    print('Stand still')
    return 'Stand still'
def chase_ball():
    print('Chase the ball')
    return 'Chase the ball'

def pass_to_teammates(players, ball):
    print('Passing the ball')
    decisions = []
    goalkeeper_number = 0  # Define the goalkeeper's number

    # Get the position of the goalkeeper
    goalkeeper_position = next(player for player in players if player['number'] == goalkeeper_number)

    # Select teammates other than the goalkeeper
    teammates = [player for player in players if player['number'] != goalkeeper_number]

    # Do nothing if there are no teammates
    if not teammates:
        return decisions

    # Logic to select the best teammate (here, simply choose the closest teammate)
    closest_teammate = min(teammates, key=lambda player: get_distance(player, ball))

    # Calculate the direction of the pass
    pass_direction = get_direction(goalkeeper_position, closest_teammate)

    # Determine the power of the pass (use a fixed value here, adjust as necessary)
    pass_power = 50  # Adjust as needed

    # Add the decision to pass
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
