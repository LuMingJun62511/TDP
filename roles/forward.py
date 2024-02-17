# forward.py
import utils
from .role import Role

class Forward(Role):
    def __init__(self, color, number):
        super().__init__(color, number)

    def move_towards_ball(self, player, ball):
        # Example action to move towards the ball
        print(f"Forward {self.number} moving towards the ball at {ball['x']}, {ball['y']}")
        direction = utils.get_direction(player, ball)
        return {
            'type': 'move',
            'player_number': self.number,
            'destination': ball,
            'direction': direction,
            'speed': 10,  # Speed might be adjusted based on the situation
        }

    def attempt_to_score(self, player, goal_position):
        # Example action to attempt scoring
        print(f"Forward {self.number} attempting to score")
        direction = utils.get_direction(player, goal_position)
        return {
            'type': 'kick',
            'player_number': self.number,
            'direction': direction,
            'power': 60,  # Power might be adjusted based on distance to goal
        }