import pygame as pg
from utils import get_direction, get_distance
from models.player import Player
import math

class Defender(Player):
    def __init__(self, x, y, name, number, color, radius, img=None, ban_cycles=0, role=None, direction=0):
        super().__init__(x, y, name, number, color, radius, img, ban_cycles, role, direction)

    def decide_action(self, ball, players):
        decisions = []
        strategic_x_min, strategic_x_max = -400, 0  # Example strategic position criteria
        strategic_y_min, strategic_y_max = -100, 100

        # Check for collision
        if self.collision_detection(ball):
            if not self.owns_ball(ball):
                decisions.append(self.execute_bounce_action(ball))

        # Ball on our half
        print("ball['x']",ball['x'])
        if ball['x'] < 0:
            # Check if the defender's team owns the ball
            if ball['owner_color'] == self.color:
                print("ball['owner_number']",ball['owner_number'])
                if self.owns_ball(ball):
                    print("self.owns_ball(ball)",self.owns_ball(ball))
                    # Try to pass if possible, otherwise move towards goal
                    pass_decision = self.pass_to_teammates(players, ball)
                    if pass_decision:
                        print("pass_decision",pass_decision)
                        decisions.append(pass_decision)
                    else:
                        decisions.append(self.move_towards_goal(ball))
                else:
                    print("self.owns_ball(ball)",self.owns_ball(ball))
                    # If not in strategic position, move there; otherwise, face the ball
                    if not self.in_strategic_position():
                        decisions.append(self.move_to_strategic_position({'x': strategic_x_max, 'y': 0}))
                    else:
                        decisions.append(self.face_ball_direction(ball))
            else:
                print("self.is_closest_to_ball(players, ball)",self.is_closest_to_ball(players, ball))
                # If the team does not own the ball
                if self.is_closest_to_ball(players, ball):
                    decisions.append(self.intercept_ball(ball))
                else:
                    decisions.append(self.move_to_strategic_position({'x': strategic_x_max, 'y': 0}))
                    print("move_to_strategic_position",self.move_to_strategic_position({'x': strategic_x_max, 'y': 0}))
        else:
            # Ball not on our half
            if not self.in_strategic_position():
                decisions.append(self.move_to_strategic_position({'x': strategic_x_max, 'y': 0}))
            else:
                decisions.append(self.face_ball_direction(ball))
        print("decisions",decisions)
        return decisions
    
    def get_strategic_position(self, ball, goal_position):
        """
        Calculate the strategic position for the defender based on the ball's position,
        the goal to defend, and the current game state.
        """
        # If the ball is in the opponent's half, position the defenders on either side of the field.
        if ball['x'] >= 0:
            # Decide which goal to defend based on their current side
            # and make sure they don't both defend the same side.
            # For simplicity, here we assume the left side of the field has negative y values.
            if self.y < 0:  # Defender is on the left side
                return {'x': -350, 'y': -100}  # Example coordinates for the left strategic point
            else:
                return {'x': -350, 'y': 100}  # Example coordinates for the right strategic point

        # If the ball is on our half but the defender's team does not own the ball
        elif ball['owner_color'] != self.color:
            # The defender closest to the ball should intercept, while the other moves to a strategic point
            if not self.is_closest_to_ball(players, ball):
                return self.calculate_midpoint_between_ball_and_goal(ball, goal_position)
            else:
                # Stay put and prepare to intercept
                return {'x': self.x, 'y': self.y}

        # If the ball is on our half and the defender's team owns the ball
        else:
            # The defender without the ball moves to a strategic point while considering the position of the ball carrier
            return self.calculate_midpoint_between_ball_and_goal(ball, goal_position)

    def calculate_midpoint_between_ball_and_goal(self, ball, goal_position):
        """
        Calculate the midpoint of the line connecting the ball and the goalpost to defend.
        If the midpoint is inside the goal, adjust the x value to leave the goal area.
        """
        mid_x = (ball['x'] + goal_position['x']) / 2
        mid_y = (ball['y'] + goal_position['y']) / 2
        # Ensure the strategic point is not inside the goal
        if mid_x < -400:  # Assuming -400 is the x-coordinate of the goal line
            mid_x = -400
        return {'x': mid_x, 'y': mid_y}
    
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
        closest_teammate = None
        min_distance = float('inf')
        for player in players:
            if player['number'] != self.number:
                distance = get_distance({'x': self.x, 'y': self.y}, {'x': player['x'], 'y': player['y']})
                if distance < min_distance:
                    closest_teammate = player
                    min_distance = distance
        
        if closest_teammate:
            direction_to_teammate = get_direction({'x': self.x, 'y': self.y}, {'x': closest_teammate['x'], 'y': closest_teammate['y']})
            return {'type': 'kick', 'player_number': self.number, 'direction': direction_to_teammate, 'power': 50}
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
    
    