import math
from utils.size import *
import pprint

## defender part
def in_strategic_position(player,strategic_position):
    return (strategic_position['x'] == player['x'] and strategic_position['y'] == player['y'])
    
def plan_running_route_and_dribble(player, ball, destination):
    # First, calculate the direction to the destination
    direction_to_goal = get_direction(player, destination)

    # Consider dribbling speed - faster when farther from opponents, slower when closer to maintain control
    # For simplicity, we'll set a fixed speed here. In a real scenario, you would adjust based on opponent positions
    dribble_speed = 7  # Adjusted for control. This could be dynamic based on context.

    # Calculate the distance to the destination to decide on dribbling aggressiveness
    distance_to_goal = get_distance(player, destination)
    if distance_to_goal > 200:  # If far from the goal, prioritize forward progress
        dribble_speed = 9
    elif distance_to_goal <= 200:  # Closer to goal, prioritize control
        dribble_speed = 5

    # Here, we could add logic to adjust the dribbling path based on the positions of opponents
    # For simplicity, this example will not include complex pathfinding or opponent avoidance

    # Update the player's position towards the goal, simulating dribbling
    # In a real scenario, you would also update the ball's position relative to the player
    print('Dribbling towards the goal')
    return {
        'type': 'move',
        'player_number': player['number'],
        'destination': destination,
        'direction': direction_to_goal,
        'speed': dribble_speed
    }
    
    
def collision_detection(player, ball):
    collision_distance = 10  # Define how close they need to be to "collide"
    current_distance = get_distance(player, ball)

    return current_distance <= collision_distance


def execute_bounce_action(player, ball):
    # Placeholder for bounce action logic after collision
    # This function can adjust the ball's direction and speed based on the collision impact
    print('Bouncing the ball away')
    # For simplicity, this will not change the ball's state in this example
    return {'type': 'move', 
            'player_number': player['number'],
            'destination': {'x': player['x'], 'y': player['y']},
            'direction': get_direction(player, ball),  # Face the ball
            'speed': 0  # Speed is 0 to only adjust the direction
            }

def move_to_strategic_position(player,strategic_position):
    # Define the strategic position (could be based on the game state)
    # strategic_position = {'x': -100, 'y': 0}  # Example position
    print('Moving to strategic position')
    return {
        'type': 'move',
        'player_number': player['number'],
        'destination': strategic_position,
        'direction': get_direction(player, strategic_position),  # Face the strategic position
        'speed': 7  # Speed adjustment could be dynamic
    }

def calculate_strategic_position_(player1, player2, ball):

    return

def calculate_strategic_position_(player1, player2, ball):

    return
def calculate_strategic_position_(player1, player2, ball):

    return


def calculate_strategic_position(player1, player2, ball):
    # center of the whole frame
    center_x = 0
    center_y = 0

    # goal post
    goalpost1_x = center_x - FOOTBALL_PITCH_LENGTH / 2
    goalpost1_y = GOAL_WIDTH / 2
    goalpost2_x = center_x - FOOTBALL_PITCH_LENGTH / 2
    goalpost2_y = -GOAL_WIDTH / 2

    # goal area
    goal_area_x_min = center_x - FOOTBALL_PITCH_LENGTH / 2
    goal_area_x_max = goal_area_x_min + GOAL_AREA_LENGTH

    # 另一位球员与两球门的距离,相对靠近一个球门,则我去守另一个,
    # 可能出现,我相比另一人,我离的两个球门都挺远,这时,还是画图吧
    # 还得再考虑,

    # 这里我必须说明一下判断的一句为什么是这样
    # 正如前述,防守的准则是补漏洞,所以,我必须看另一个队友,他相对缺少防守的一侧要交给我,因为他可能在追球,

    # 如果,两个人都这么搞,很可能,他们会同时放弃离自己相对近的球门,转而向远侧跑,而且,这样的情况是可能发生的,就出现在球在我方半场,本队持球,
    distance_player2_to_goalpost1 = ((player2['x'] - goalpost1_x)**2 + (player1['y'] - goalpost1_y)**2)**0.5
    distance_player2_to_goalpost2 = ((player2['x'] - goalpost1_x)**2 + (player2['y'] - goalpost1_y)**2)**0.5

    # 观察另一位球员离哪侧近,他守离他近的,我守另一侧,不行,还是有问题,如果都在一侧,那就都往远侧跑了,
    if distance_player2_to_goalpost1 <= distance_player2_to_goalpost2:
        # player2 closer to goalpost2 我离球门1更近,不一定我就离球门二更远,有可能你在场外侧,你相对我离两个球门都远,
        defend_goalpost_x, defend_goalpost_y = goalpost2_x, goalpost2_y
    else:
        # player2 closer to goalpost1
        defend_goalpost_x, defend_goalpost_y = goalpost1_x, goalpost1_y

    # 计算球和防守门柱的连线中点
    midpoint_x = (ball['x'] + defend_goalpost_x) / 2
    midpoint_y = (ball['y'] + defend_goalpost_y) / 2

    # 确保战略点不在球门区内
    if midpoint_x < goal_area_x_max:
        midpoint_x = goal_area_x_max

    strategic_position = {'x': midpoint_x, 'y': midpoint_y}
    return strategic_position




def face_ball_direction(player, ball):
    # Adjust player's orientation to face the ball
    print('Facing ball direction')
    direction_to_ball = get_direction(player, ball)
    # This example does not change the player's state but could in a full implementation
    return {
        'type': 'move',
        'player_number': player['number'],
        'destination': {'x': player['x'], 'y': player['y']},  # Stay in place
        'direction': direction_to_ball,
        'speed': 0  # Speed is 0 to only adjust the direction
    }

def intercept_ball(player, ball):
    # Move towards the ball to intercept it
    print('Intercepting the ball')
    return {
        'type': 'move',
        'player_number': player['number'],
        'destination': ball,
        'speed': 10  # Speed could be adjusted based on urgency
    }
    
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
        'direction':get_direction(goalkeeper,ball),
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

def defend_ball(player, ball):
    # Define the defensive action
    print('Defending the ball')
    player_x, player_y = player['x'], player['y']
    ball_x, ball_y = ball['x'], ball['y']
    
    # Calculate the direction to the ball and move towards it
    direction_to_ball = get_direction(player, ball)
    
    # Define a simple logic to move towards the ball aggressively
    return {
        'type': 'move',
        'player_number': player['number'],
        'destination': {'x': ball_x, 'y': ball_y},
        'direction': direction_to_ball,
        'speed': 10  # Adjust the speed as needed
    }


# Based on the above code,
def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    
    ### goal keeper
    if ball['x'] < 0:  # Is the ball on our half of the field?
        print('ball', ball)
        
        if -460 < ball['x'] < -300:
           # Find the defender (player number 1)
            defender = next((player for player in red_players if player['number'] == 1), None)
            if defender:
                # Defender takes action
                decision = defend_ball(defender, ball)
                decisions.append(decision)
                    
                    
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
                    'direction':get_direction(red_players[0],ball),
                    'speed': 10,
                })
        else:  # The ball is on our half of the field, but not in the penalty area
            decision = adjust_self(red_players, ball, 160, 210)  
            decisions.append(decision)
    else:  # The ball is not on our half of the field
        stand_still()  # Can trigger
            
    ## defender
    # defender = next((player for player in red_players if player['number'] == 1), None)
    defender = next((player for player in red_players if player['number'] == 1), None)
    defender2 = next((player for player in red_players if player['number'] == 2), None)

    # 假设ball是一个字典，包含球的位置信息
    ball_position = {'x': ball['x'], 'y': ball['y']}

    
    # Check for collision first
    if collision_detection(defender, ball):
        if not ball.get('owner_number') == 1:  # If defender does not own the ball
            decisions.append(execute_bounce_action(defender, ball))
    
    print("Starting ball position check.")
    if ball['x'] < 0:  # Ball is on our half of the field
        print("Ball is on our half of the field.")
        if defender and 'owner_number' in ball and ball['owner_number'] == 1:  # Defender owns the ball
            print("Defender owns the ball.")
            # Attempt to pass to a teammate or move towards goal if no pass option
            pass_decision = pass_to_teammates(red_players, ball)
            if pass_decision:  # If a pass is possible
                print("Passing to a teammate.")
                decisions.append(pass_decision)
            else:  # Move towards the goal
                print("No teammate to pass to, moving towards goal.")
                decisions.append(plan_running_route_and_dribble(defender, ball, {'x': 0, 'y': defender['y']}))
        elif not 'owner_number' in ball or ball['owner_number'] != 1:  # Defender does not own the ball
            print("Defender does not own the ball.")
            # Check if in strategic position
            strategic_position = 
            if in_strategic_position(defender,strategic_position):  # Assuming this function checks the player's position
                print("Defender is in strategic position, facing ball direction.")
                decisions.append(face_ball_direction(defender, ball))
            else:
                print("Defender is not in strategic position, moving to it.")
                decisions.append(move_to_strategic_position(defender,strategic_position))
            # Additional logic to intercept the ball if closer than teammates could be added here
    else:  # Ball is not on our half of the field
        print("Ball is not on our half of the field.")
        strategic_position = 
        if in_strategic_position(defender,strategic_position):  # Assuming this function checks the player's position
            print("Defender is in strategic position, facing ball direction.")
            decisions.append(face_ball_direction(defender, ball))
        else:
            print("Defender is not in strategic position, moving to it.")
            decisions.append(move_to_strategic_position(defender,strategic_position))


    pprint.pprint(decisions)
    return decisions
