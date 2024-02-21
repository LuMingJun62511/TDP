import random
import exception
import utils
from .decision import Decision

class GrabDecision(Decision):
    def __init__(self, runner, player_number, player_color,direction):
        super().__init__(runner, player_number, player_color)
        # self.direction = direction
    

    def perform(self):
        if self._can_grab():
            self._grab_ball()
    
    def _can_grab(self):
        grab_radius = 18  # 修改抓取半径为18
        distance = utils.distance(self.runner.ball, self.player)
        if distance < grab_radius:
            return True
        return False
    
    def _grab_ball(self):
        grab_radius = 18
        min_distance = float('inf')  # 初始化最小距离为正无穷大
        closest_player = None
        
        for player in self.runner.players:
            distance = utils.distance(player, self.runner.ball)
            if distance < grab_radius and distance < min_distance:
                min_distance = distance
                closest_player = player

        if closest_player is not None:
            self.runner.ball.owner = closest_player
            self.runner.ball.direction = closest_player.direction
            print("当前持球人是",self.runner.ball.owner.color,self.runner.ball.owner.number)



