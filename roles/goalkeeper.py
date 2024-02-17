import pygame as pg
import utils
from .role import Role

class GoalKeeper(Role):
    def __init__(self, color, number):
        super().__init__(color, number)
        self.position = {'x': 0, 'y': 0}  # Assuming initial position

    def adjust(self, x, y, direction):
        self.position['x'] = x
        self.position['y'] = y
        self.direction = direction

    def is_in_own_penalty_area(self):
        # Assuming the penalty area dimensions are defined somewhere
        return utils.is_in_penalty_area(self.position, self.color)

    def kick(self, direction, power):
        # Placeholder for kicking logic. In a real game, this would interact with the ball object.
        print(f"Kicking in direction {direction} with power {power}")

    def decide_action(self, ball, players):
        decisions = []
        if ball['x'] < -460:
            decisions.append(self.serve_ball())
        elif ball['x'] < 0:
            if ball['x'] < -300:
                if ball['owner_number'] == self.number:
                    decisions.append(self.pass_to_teammates(players, ball))
                else:
                    decisions.append(self.chase_ball(ball))
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
        direction = utils.get_direction(self.position, ball)
        return {'type': 'move', 'player_number': self.number, 'destination': ball['position'], 'direction': direction, 'speed': 10}

    def pass_to_teammates(self, players, ball):
        print('Passing to teammates')
        # Simplified passing logic
        teammate = self.find_closest_teammate(players)
        if teammate:
            direction = utils.get_direction(self.position, teammate['position'])
            return {'type': 'kick', 'player_number': self.number, 'direction': direction, 'power': 50}
        else:
            return None

    def find_closest_teammate(self, players):
        # Find the closest teammate to pass the ball to
        closest_distance = float('inf')
        closest_player = None
        for player in players:
            if player['number'] != self.number:
                distance = utils.get_distance(self.position, player['position'])
                if distance < closest_distance:
                    closest_distance = distance
                    closest_player = player
        return closest_player

    def adjust_self(self, players, ball):
        # Simplified logic to adjust position based on the ball's position
        print('Adjusting position')
        direction = utils.get_direction(self.position, ball['position'])
        return {'type': 'move', 'player_number': self.number, 'destination': ball['position'], 'direction': direction, 'speed': 5}

    def stand_still(self):
        print('Standing still')
        return {'type': 'move', 'player_number': self.number, 'destination': self.position, 'direction': 0, 'speed': 0}
