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
        strategic_pos = self.determine_strategic_position(ball, players)

        # Collision detection and ball ownership checks
        # if self.collision_detection(ball) and not self.owns_ball(ball):
        #     decisions.append(self.execute_bounce_action(ball))

        # Ball on our half
        if ball['x'] < 0:
            if self.color == ball['owner_color']:  # Our team has the ball
                if self.owns_ball(ball):
                    decisions.append(self.pass_to_teammates(players, ball))
                else:
                    decisions.append(self.move_to_strategic_position(strategic_pos))
            else:  # Opponent team has the ball
                if self.is_closest_to_ball(players, ball):
                    decisions.append(self.intercept_ball(ball))
                else:
                    decisions.append(self.move_to_strategic_position(strategic_pos))
        else:
            decisions.append(self.move_to_strategic_position(strategic_pos))

        return decisions

    def determine_strategic_position(self, ball, players):
        if ball['x'] < 0:
            if self.color == ball['owner_color']:
                return self.calculate_offensive_strategic_position(ball, players)
            else:
                return self.calculate_defensive_strategic_position(ball, players)
        else:
            return self.default_strategic_position()

    def default_strategic_position(self):
        return {'x': -200, 'y': 0} if self.color == 'red' else {'x': 200, 'y': 0}

    def calculate_defensive_strategic_position(self, ball, players):
        # Based on the midpoint between the ball and the most threatened goalpost
        goal_x = -500 if self.color == 'red' else 500
        goal_y = 0
        midpoint_x = (ball['x'] + goal_x) / 2
        # Ensure the defender doesn't position inside the goal area
        if self.color == 'red':
            midpoint_x = max(midpoint_x, -400)  # Adjust based on field dimensions
        else:
            midpoint_x = min(midpoint_x, 400)
        return {'x': midpoint_x, 'y': goal_y}

    def calculate_offensive_strategic_position(self, ball, players):
        # Determine position based on attacking opportunities
        return {'x': 100, 'y': 0} if self.color == 'red' else {'x': -100, 'y': 0}
    
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

    # New or refined methods based on the strategic positioning requirements
    def move_to_strategic_position(self, strategic_pos):
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': strategic_pos,
            'direction': direction_to_strategic_pos,
            'speed': 7
        }
    
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
    
    