import pygame as pg
import utils
from .role import Role


class Forward(Role):
    def __init__(self,color,number):
        super().__init__(color,number)
        
