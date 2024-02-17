import pygame as pg
import utils
from .role import Role


class GoalKeeper(Role):
    def __init__(self,color,number):
        super().__init__(color,number)
        

    def adjust(self,x,y,direction):
        self.direction = direction
        self.x = x
        self.y = y

    def is_in_own_penalty_area(self):
        if self.color == 'red':
            x_1 = 1
            x_2 = 1
            y_1 = 1
            y_2 = 1
        elif self.color == 'blue':
            x_1 = 2
            x_2 = 2
            y_1 = 2
            y_2 = 2
        if self.x < x_1 and self.x > x_2 and self.y < y_1 and self.y > y_2:
            return True
        else:
            return False

    def kick(self,direction,power):
        self.direction = direction
        self.power = power

    
    