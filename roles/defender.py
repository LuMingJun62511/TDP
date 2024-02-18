import pygame as pg
from utils import get_direction, get_distance
from models.player import Player
import math
import pprint

class Defender(Player):
    def __init__(self, x, y, name, number, color, radius, img=None, ban_cycles=0, role=None, direction=0):
        super().__init__(x, y, name, number, color, radius, img, ban_cycles, role, direction)

    def decide_action(self, ball, players):
        decisions = []
        # Define the strategic position based on the ball's location and possession status
        strategic_position = self.calculate_strategic_position(ball, players)
        
        # if self.collision_detection(ball):
        #     print("Defender is colliding with the ball")
        #     if not self.owns_ball(ball):
        #         print("Defender does not own the ball")
        #         decisions.append(self.execute_bounce_action(ball))

        # Check if in strategic position, if not, move there; otherwise, consider passing or intercepting
        if not self.in_strategic_position():
            print("Defender is not in strategic position")
            decisions.append(self.move_to_strategic_position(strategic_position))
        else:
            if ball['x'] < 0:
                print("Defender is in strategic position")
                if ball['owner_color'] == self.color:
                    if self.owns_ball(ball):
                        print("Defender owns the ball")
                        pass_decision = self.pass_to_teammates(players, ball)
                        if pass_decision:
                            print("Defender is passing the ball")
                            decisions.append(pass_decision)
                        else:
                            print("Defender is moving towards goal")
                            decisions.append(self.move_towards_goal(ball))
                    else:
                        print("Defender does not own the ball")
                        decisions.append(self.face_ball_direction(ball))
                else:
                    print("Defender is not in possession")
                    if self.is_closest_to_ball(players, ball):
                        decisions.append(self.intercept_ball(ball))
                    else:
                        decisions.append(self.face_ball_direction(ball))
            else:
                print("Defender is in strategic position")
                decisions.append(self.face_ball_direction(ball))
        print("Defender Decisions: ")
        pprint.pprint(decisions)
        return decisions

    def calculate_strategic_position(self, ball, players):
        # Implement logic based on documentation
        if ball['x'] >= 0:
            # Scenario 1: Ball not on our half
            return self.default_strategic_position()
        else:
            # Scenario 2 and 3: Ball on our half
            if ball['owner_color'] != self.color or not self.is_closest_to_ball(players, ball):
                # Move to a position that covers the farthest goal from the ball
                return self.calculate_defensive_strategic_position(ball, players)
            else:
                # Scenario when we own the ball or are closest to it
                return self.calculate_offensive_strategic_position(ball, players)

    def default_strategic_position(self):
        # Return a default strategic position based on the side of the field
        return {'x': -300, 'y': 0}  # Example value

    def calculate_defensive_strategic_position(self, ball, players):
        # Calculate defensive position based on ball and goal locations
        # Implement logic from documentation
        return {'x': -350, 'y': 0}  # Placeholder logic

    def calculate_offensive_strategic_position(self, ball, players):
        # Calculate offensive position when in possession but not holding the ball
        # Implement logic from documentation
        return {'x': -200, 'y': 0}  # Placeholder logic
    
    def in_strategic_position(self):
        # Check if the defender is in a strategic position
        strategic_x_min, strategic_x_max = -400, 0
        strategic_y_min, strategic_y_max = -100, 100
        return strategic_x_min <= self.x <= strategic_x_max and strategic_y_min <= self.y <= strategic_y_max

    def move_to_strategic_position(self, strategic_pos):
        # Move to a predefined strategic position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7
        }

    def collision_detection(self, ball):
        # Adjusted to use 'x' and 'y' directly
        return get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']}) <= 10

    def owns_ball(self, ball):
        return ball['owner_number'] == self.number

    def execute_bounce_action(self, ball):
        direction_away_from_ball = get_direction({'x': ball['x'], 'y': ball['y']}, {'x': self.x, 'y': self.y})
        return {'type': 'move', 'player_number': self.number, 'direction': direction_away_from_ball, 'speed': 0}

    def pass_to_teammates(self, players, ball):
        most_advanced_teammate = None
        max_advance_x = -float('inf')  # Initialize with a very small number

        for player in players:
            if player['number'] != self.number and player['role'] != 'goalkeeper':
                # Check if this player is more advanced towards the opponent's goal
                if player['x'] > max_advance_x:
                    most_advanced_teammate = player
                    max_advance_x = player['x']
        
        if most_advanced_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': most_advanced_teammate['x'], 'y': most_advanced_teammate['y']})
            return {
                'type': 'kick',
                'player_number': self.number,
                'direction': direction_to_teammate,
                'power': 50  # Adjust power as necessary
            }
        else:
            return None

    def move_towards_goal(self, ball):
        goal_position = {'x': 500, 'y': 0}
        direction_to_goal = get_direction({'x': self.x, 'y': self.y}, goal_position)
        return {'type': 'move', 'player_number': self.number, 'destination': goal_position, 'direction': direction_to_goal, 'speed': 7}

    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {'type': 'move', 'player_number': self.number, 'destination': {'x': self.x, 'y': self.y}, 'direction': direction_to_ball, 'speed': 0}

    def move_to_strategic_position(self, strategic_position):
        strategic_pos = strategic_position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {'type': 'move', 'player_number': self.number, 'destination': strategic_pos, 'direction': direction_to_strategic_pos, 'speed': 7}
        
    def is_closest_to_ball(self, players, ball):
        """Check if this defender is the closest to the ball among all players."""
        own_distance = get_distance({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        for player in players:
            if player['number'] != self.number:
                if get_distance({'x': player['x'], 'y': player['y']}, {'x': ball['x'], 'y': ball['y']}) < own_distance:
                    return False
        return True

    def intercept_ball(self, ball):
        """Move towards the ball to intercept it."""
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': {'x': ball['x'], 'y': ball['y']},
            'direction': direction_to_ball,
            'speed': 10  # This speed can be adjusted based on gameplay needs
        }
    
    