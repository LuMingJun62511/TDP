import pygame as pg
import utils
from .role import Role


class Defender(Role):
    def __init__(self, color, number):
        super().__init__(color, number)
    
    def defend_ball(self, ball, players):
        # Example defensive action
        print(f"Defender {self.number} is defending against the ball at {ball['x']}, {ball['y']}")
        # Add logic to move towards the ball, intercept passes, or clear the ball away