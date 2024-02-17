# forward.py
import utils
from .role import Role
from models import player

class Forward(player.Player):
    def __init__(self, x,y,name, number, color,radius,img=None, ban_cycles=0,role=None,direction=0):
        super().__init__(x,y,name, number, color,radius,img, ban_cycles,role,direction)

    def decide_action(self, ball, players, own_half, strategic_position):
        return super().decide_action(ball, players, own_half, strategic_position)

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