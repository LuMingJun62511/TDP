import exception
from utils import utils
import math
from .decision import Decision
from .grab import GrabDecision
from models import Point


class Collision(Decision):
    def __init__(self, runner, player_number, player_color,direction):
        super().__init__(runner, player_number, player_color)
        self.direction = direction
        #self.speed = speed

    
    def _can_collision(self):
        min_distance = 25
        max_angle_degrees = 120

        for player in self.runner.players:
            if player != self.player:  # 排除当前球员自身
                distance = utils.distance(player, self.player)
                angle = utils._cal_angle(player,self.player)
                #print(angle,"jihao",player.number,distance)
                if distance < min_distance and angle < max_angle_degrees:
                    return True
        return False

    def perform(self):
        if self._can_collision():
            print("发生碰撞")
            if self.runner.ball.owner is not None and self.runner.ball.owner != self.player:
                print(self.player.color,self.player.number,"改变方向",self.player.direction)
                direction = -self.player.direction
                x = self.player.x + int(18 * math.cos(direction))
                y = self.player.y + int(18 * math.sin(direction))
                destination = Point(x,y)
                self.player.move(destination,direction,10)
        elif GrabDecision._can_grab(self):
            self.runner.ball.owner = self.player
            print("截断成功")
        
            
       
        