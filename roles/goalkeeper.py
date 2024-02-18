import pygame as pg
from utils import FOOTBALL_PITCH_LENGTH,GOAL_DEPTH,PLAYER_RADIUS
from .role import Role
from utils import utils 
from models import player
class GoalKeeper(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)


    def is_in_own_penalty_area(self):
        # Assuming the penalty area dimensions are defined somewhere
        return utils.is_in_penalty_area({'x': self.x, 'y': self.y}, self.color)
    
    def is_in_goal_area(self,ball):
        if self.color == 'red':
            x = ball['x']
            y = ball['y']
            x1 = -450
            x2 = -350
            y1 = -150
            y2 = 150
        elif self.color == 'blue':
            x = ball['x']
            y = ball['y']
            x1 = 350
            x2 = 450
            y1 = -150
            y2 = 150
        else:
            print("错误的守门员属性")
        return x1 < x < x2 and y1 < y < y2
    
    def own_half(self,ball):
        if self.color == 'red':
            x = ball['x']
            x1 = -450
            x2 = 0
        elif self.color == 'blue':
            x = ball['x']
            x1 = 0
            x2 = 450
        else:
            print("错误的守门员属性")
        return x1 < x < x2
    def kick(self, direction, power):
        # Placeholder for kicking logic. In a real game, this would interact with the ball object.
        print(f"Kicking in direction {direction} with power {power}")

    def decide_action(self, ball, players):
        decisions = []
        if self.own_half(ball):
            if self.is_in_goal_area(ball):
                if ball['owner_number'] == self.number:
                    decisions.append(self.pass_to_teammates(players, ball))
                else:
                    decisions.append(self.serve_ball())
            else:
                decisions.append(self.adjust_self(players, ball))
        else:
            decisions.append(self.stand_still())
        return decisions

    def serve_ball(self):
        print('Picking up the ball')
        return {'type': 'grab', 'player_number': self.number}

    def chase_ball(self, ball):
        print('Chasing the ball')
        direction = utils.get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {'type': 'move', 'player_number': self.number, 'destination': {'x': ball['x'], 'y': ball['y']}, 'direction': direction, 'speed': 10}

    def pass_to_teammates(self, players, ball):
        print('Passing to teammates')
        teammate = self.find_closest_teammate(players)
        if teammate:
            direction = utils.get_direction({'x': self.x, 'y': self.y}, {'x': teammate['x'], 'y': teammate['y']})
            return {'type': 'kick', 'player_number': self.number, 'direction': direction, 'power': 50}
        else:
            return None

    def find_closest_teammate(self, players):
        closest_distance = float('inf')
        closest_player = None
        for player in players:
            if player['number'] != self.number:
                distance = utils.get_distance({'x': self.x, 'y': self.y}, {'x': player['x'], 'y': player['y']})
                if distance < closest_distance:
                    closest_distance = distance
                    closest_player = player
        return closest_player

    def adjust_self(self, players, ball):
        print('Adjusting position')
        direction = utils.get_direction({'x': self.x, 'y': self.y}, {'x': ball['x'], 'y': ball['y']})
        return {'type': 'move', 'player_number': self.number, 'destination': {'x': ball['x'], 'y': ball['y']}, 'direction': direction, 'speed': 0}

    def stand_still(self):
        print('Standing still')
        if self.color == 'red':
            return {'type': 'move', 'player_number': self.number, 'destination': {'x':  -FOOTBALL_PITCH_LENGTH // 2 + 3 * GOAL_DEPTH, 'y': 0}, 'direction': 0, 'speed': 8}
        elif self.color == 'blue':
            return {'type': 'move', 'player_number': self.number, 'destination': {'x':  FOOTBALL_PITCH_LENGTH // 2 - 3 * GOAL_DEPTH, 'y': 0}, 'direction': 0, 'speed': 8}
        else:
            print("错误的守门员属性")