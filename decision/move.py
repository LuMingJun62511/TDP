import exception
from utils import utils,game,size
from .decision import Decision
import math

class MoveDecision(Decision):
    def __init__(self, runner, player_number, player_color, destination,direction, speed):
        super().__init__(runner, player_number, player_color)
        self.destination = destination
        self.direction = direction
        self.speed = speed

    def validate(self):
        super().validate()
        if not 0 <= self.speed <= game.MAX_PLAYER_SPEED:
            raise exception.DecisionException('Wrong move speed')
        if not -size.FOOTBALL_PITCH_LENGTH // 2 < self.destination.x < size.FOOTBALL_PITCH_LENGTH // 2 or \
                not -size.FOOTBALL_PITCH_WIDTH // 2 < self.destination.y < size.FOOTBALL_PITCH_WIDTH // 2:
            raise exception.DecisionException('Cannot move out of screen')

    def perform(self):
        #self.player.move(self.destination,self.direction, self.speed)
        distance = utils.distance(self.player, self.destination)
        alpha = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
        
        if distance < self.speed:
            self.player.x = int(self.destination.x)
            self.player.y = int(self.destination.y)
            self.player.direction = alpha
        
        else:
            alpha = math.atan2((self.destination.y - self.player.y), (self.destination.x - self.player.x))
            #alpha = direction
            self.player.x += int(self.speed * math.cos(alpha))
            self.player.y += int(self.speed * math.sin(alpha))
            self.player.direction = alpha
            self.player.speed = self.speed
