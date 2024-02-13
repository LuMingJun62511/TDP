import exception
import utils
from .decision import Decision


class Collision(Decision):
    def __init__(self, runner, player_number, player_color, direction, speed):
        super().__init__(runner, player_number, player_color)
        self.direction = direction
        self.speed = speed

    def _can_collision(self):
        min_distance = 15
        for player in self.runner.players:
            if player != self.player:  # 排除当前球员自身
                distance = utils.distance(player, self.player)
                if distance < min_distance:
                    return True
        return False

    def perform(self):
        if self._can_collision():
            self.direction = -self.direction
            print("发生了碰撞")
        