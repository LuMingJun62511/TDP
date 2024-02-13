import math

import pygame as pg

import utils
from .point import Point
from roles import goalkeeper,defender,forward

class Player:
    def __init__(self, x, y, name, number, color, radius=utils.PLAYER_RADIUS, img=None, ban_cycles=0,role=None):
        img_link = utils.RED_PLAYER_IMG_LINK
        if color == 'blue':
            img_link = utils.BLUE_PLAYER_IMG_LINK
        default_img = pg.image.load(img_link)
        default_img = pg.transform.scale(default_img, (2 * radius, 2 * radius))
        default_img.convert_alpha()
        self.x = x
        self.y = y
        self.name = name
        self.number = number
        self.color = color
        self.radius = radius
        self.img = img or default_img
        self.ban_cycles = ban_cycles
        if role == 'goalkeeper':
            self.role = goalkeeper.GoalKeeper(color,number)
        elif role == 'defender':
            self.role = defender.Defender(self.color,self.number)
        elif role == 'forward':
            self.role = forward.Forward(self.color,self.number)
        else:
            print("wrong role!")

    def draw(self, screen):
        pygame_x, pygame_y = utils.convert_coordinate_cartesian_to_pygame(self.x , self.y)
        screen.blit(self.img, (int(pygame_x)-self.radius, int(pygame_y)-self.radius))
        utils.write_text_on_pygame_screen(
            screen,
            utils.PLAYER_NUMBER_FONT_SIZE,
            utils.PLAYER_TEXTS_COLOR,
            str(self.number),
            self.x - self.radius // 2,
            self.y + self.radius // 2,
        )
        utils.write_text_on_pygame_screen(
            screen,
            utils.PLAYER_NAME_FONT_SIZE,
            utils.PLAYER_TEXTS_COLOR,
            self.name,
            self.x - self.radius,
            self.y - self.radius,
        )

    def move(self, destination, speed):
        distance = utils.distance(self, destination)
        if distance < speed:
            self.x = int(destination.x)
            self.y = int(destination.y)
        else:
            alpha = math.atan2((destination.y - self.y), (destination.x - self.x))
            self.x += int(speed * math.cos(alpha))
            self.y += int(speed * math.sin(alpha))

    def is_in_own_penalty_area(self):
        if self.color == 'red':
            p = Point(-utils.FOOTBALL_PITCH_WIDTH // 2, 0)
        elif self.color == 'blue':
            p = Point(utils.FOOTBALL_PITCH_WIDTH // 2, 0)
        if utils.distance(self, p) < utils.PENALTY_AREA_WIDTH:
            return True
        else:
            return False
        

    def role(self):
        if self.role == 'goalkeeper':
            role = goalkeeper.GoalKeeper(self,self.color,self.number)
        elif self.role == 'defender':
            role = defender.Defender(self,self.color,self.number)
        elif self.role == 'forward':
            role = forward.Forward(self,self.color,self.number)
        #需要异常处理
        else:
            print("不匹配的身份定义")
        
        return role

    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles
        }

    @property
    def info_reversed(self):
        return {
            'x': -self.x,
            'y': -self.y,
            'name': self.name,
            'number': self.number,
            'radius': self.radius,
            'ban_cycles': self.ban_cycles,
        }
