import math
from roles import goalkeeper, defender, forward

# Assuming the existence of utility functions get_direction and get_distance
# These functions compute the direction and distance between two points



def play(red_players, blue_players, ball, scoreboard):
    decisions = []
    goal_position = {'x': 500, 'y': 0}  # Example goal position for scoring

    # Define strategic position criteria for this example
    def is_in_strategic_position(player):
        strategic_x_min, strategic_x_max = -400, 0  # Half of the field for red team
        strategic_y_min, strategic_y_max = -100, 100  # Middle strip of the field
        return (strategic_x_min <= player.x <= strategic_x_max and
                strategic_y_min <= player.y <= strategic_y_max)

    # Define own half based on the ball's position for the red team
    def own_half(ball):
        return ball['x'] < 0

    # Loop through each player in the red team
    for player in red_players:
        print('player', player)
        # Depending on the role, call the appropriate decision-making function
        if isinstance(player['role'], goalkeeper.GoalKeeper):
            print('player is goalkeeper')
            # For a goalkeeper, additional conditions based on the ball's position could be implemented
            if ball['x'] < -460:
                print('ball', ball)
                decisions.append(player.serve_ball())
            elif ball['x'] < 0:
                print('ball', ball)
                if ball['x'] < -300 and ball.get('owner_number') != player['number']:
                    print('ball', ball)
                    decisions.append(player.chase_ball(ball))
                else:
                    decisions.append(player.stand_still())
            else:
                decisions.append(player.stand_still())
        elif isinstance(player['role'], defender.Defender):
            # Defenders make decisions based on ball possession and strategic positioning
            strategic_decision = player.action_decision(ball, red_players, own_half, is_in_strategic_position)
            decisions.extend(strategic_decision)
        elif isinstance(player['role'], forward.Forward):
            # Forwards could have their own logic for attacking plays or positioning
            # This could involve moving towards the goal, attempting shots, or positioning for passes
            # Placeholder for forward decision logic
            pass
        else:
            print(f"Unrecognized player role for player {player['number']}")

    return decisions


