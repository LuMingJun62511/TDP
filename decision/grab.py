import random
import exception
import utils
from .decision import Decision
import math
import time
class GrabDecision(Decision):
    def __init__(self, runner, player_number, player_color,direction):
        super().__init__(runner, player_number, player_color)
        # self.direction = direction
    

    def perform(self):
        if self._can_grab():
            self._grab_ball()
    
    def _can_grab(self):
        grab_radius = 24  # The radius of the player's grabbing range
        distance = utils.distance(self.runner.ball, self.player)
        if distance <= grab_radius:
            return True
        return False
    
    def _grab_ball(self):
        grab_radius = 24  # The radius of the player's grabbing range
        min_distance = float('inf')  # 初始化最小距离为正无穷大
        closest_player = None
        
        for player in self.runner.players:
            distance = utils.distance(player, self.runner.ball)
            if distance < grab_radius and distance < min_distance:
                min_distance = distance
                closest_player = player

        # if closest_player is not None:
        #     self.runner.ball.owner = closest_player
        #     self.runner.ball.direction = closest_player.direction
        #     print("当前持球人是",self.runner.ball.owner.color,self.runner.ball.owner.number)

        if closest_player:
            # sleep 1 second
            self.runner.ball.owner = closest_player
            # Here you should also set the ball's position relative to the player
            # This might need information about from which direction the ball was grabbed, which could be tracked.
            ball_direction = math.radians(closest_player.direction)
            self.runner.ball.x = closest_player.x + (closest_player.radius + self.runner.ball.radius) * math.cos(ball_direction)
            self.runner.ball.y = closest_player.y + (closest_player.radius + self.runner.ball.radius) * math.sin(ball_direction)


