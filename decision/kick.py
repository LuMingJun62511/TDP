import exception
import utils
from .decision import Decision


class KickDecision(Decision):
    def __init__(self, runner, player_number, player_color, direction, power):
        super().__init__(runner, player_number, player_color)
        self.player_number = player_number
        self.direction = direction
        self.power = power

    def validate(self):
        super().validate()
        if not 0 <= self.power <= utils.MAX_KICK_POWER:
            raise exception.DecisionException('Wrong kick power')
        if self.runner.ball.owner.number != self.player_number:
            raise exception.DecisionException('The player is not the owner of the ball') 

    def perform(self):
        print(self.direction,"dicision 获取到的方向")
        self.runner.ball.owner = None
        self.runner.ball.direction = self.direction
        self.runner.ball.speed = self.power
