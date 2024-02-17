import pygame as pg
from utils import get_direction, get_distance
from .role import Role
import math
from models import player

class Defender(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players, own_half, strategic_position):
        decisions = []
        decisions.append({
            'type':'collision',
            'player_number': self.number,
            'direction': get_direction({'x': ball['x'], 'y': ball['y']}, {'x': self.x, 'y': self.y}), 
        })

        if self.collision_detection(ball):
            if not self.owns_ball(ball):
                decisions.append(self.execute_bounce_action(ball))
        
        if ball['x'] in own_half:
            if self.owns_ball(ball):
                pass_decision = self.pass_to_teammates(players, ball)
                if pass_decision:
                    decisions.append(pass_decision)
                else:
                    decisions.append(self.move_towards_goal(ball))
            elif self.in_strategic_position(strategic_position, self):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))
        else:
            if self.in_strategic_position(strategic_position, self):
                decisions.append(self.face_ball_direction(ball))
            else:
                decisions.append(self.move_to_strategic_position(strategic_position))

        return decisions

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

    def in_strategic_position(self, strategic_position, player):
        #return strategic_position(player)
        return player in strategic_position

    def face_ball_direction(self, ball):
        direction_to_ball = get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {'type': 'move', 'player_number': self.number, 'destination': {'x': self.x, 'y': self.y}, 'direction': direction_to_ball, 'speed': 0}

    def move_to_strategic_position(self, strategic_position):
        strategic_pos = strategic_position
        direction_to_strategic_pos = get_direction({'x': self.x, 'y': self.y}, strategic_pos)
        return {'type': 'move', 'player_number': self.number, 'destination': strategic_pos, 'direction': direction_to_strategic_pos, 'speed': 7}
    
    