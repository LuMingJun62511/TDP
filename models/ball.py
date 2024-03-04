import math

import pygame as pg

import utils


class Ball:
    def __init__(self, x=None, y=None, radius=None, img=None, owner=None, speed=None, direction=None):
        default_ball_image = pg.image.load(utils.BALL_IMG_LINK)
        default_ball_image = pg.transform.scale(default_ball_image, (2 * utils.BALL_RADIUS, 2 * utils.BALL_RADIUS))
        default_ball_image.convert_alpha()
        self.x = x or 0
        self.y = y or 0
        self.radius = radius or utils.BALL_RADIUS
        self.img = img or default_ball_image
        self.owner = owner
        self.speed = speed or 0
        self.direction = direction

    def draw(self, screen):
        pygame_x, pygame_y = utils.convert_coordinate_cartesian_to_pygame(self.x, self.y)
        screen.blit(
            self.img,
            (int(pygame_x) - self.radius, int(pygame_y) - self.radius)
        )
    def move(self):
        if self.owner is not None:
            # Logic when the ball is with a player
            ball_placement_angle = 180 if self.owner.color == 'blue' else 0  # Blue faces right, red faces left.
            placement_direction = math.radians(self.owner.direction + ball_placement_angle)
            self.x = self.owner.x + (self.owner.radius + self.radius) * math.cos(placement_direction)
            self.y = self.owner.y + (self.owner.radius + self.radius) * math.sin(placement_direction)
            #self.x = self.owner.x + (self.owner.radius + self.radius) * math.cos(math.radians(self.owner.direction))
            #self.y = self.owner.y + (self.owner.radius + self.radius) * math.sin(math.radians(self.owner.direction))
        elif self.direction is not None:
            if self.speed == 0 or self.direction is None:
                return
            self.x += self.speed * math.cos(math.radians(self.direction))
            self.y += self.speed * math.sin(math.radians(self.direction))
            self.speed -= utils.FRICTION
            if self.speed < 0:
                self.speed = 0
                self.direction = None

            # Check for goal conditions
            if self.x < -utils.FOOTBALL_PITCH_LENGTH // 2 and not (-utils.GOAL_WIDTH // 2 <= self.y <= utils.GOAL_WIDTH // 2):
                self.x = -utils.FOOTBALL_PITCH_LENGTH // 2 + self.radius + 1
                self.direction = (180 - self.direction) % 360
            elif self.x > utils.FOOTBALL_PITCH_LENGTH // 2 and not (-utils.GOAL_WIDTH // 2 <= self.y <= utils.GOAL_WIDTH // 2):
                self.x = utils.FOOTBALL_PITCH_LENGTH // 2 - self.radius - 1
                self.direction = (180 - self.direction) % 360

            # Boundary conditions for top and bottom
            if self.y < -utils.FOOTBALL_PITCH_WIDTH // 2:
                self.y = -utils.FOOTBALL_PITCH_WIDTH // 2 + self.radius + 1
                self.direction = (360 - self.direction) % 360
            elif self.y > utils.FOOTBALL_PITCH_WIDTH // 2:
                self.y = utils.FOOTBALL_PITCH_WIDTH // 2 - self.radius - 1
                self.direction = (360 - self.direction) % 360
        else:
            print("默认")
            self.x = self.owner.x + 12
            self.y = self.owner.y + 12


    @property
    def info(self):
        return {
            'x': self.x,
            'y': self.y,
            'radius': self.radius,
            'owner_color': None if self.owner is None else self.owner.color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': self.direction,
            'speed': self.speed,
        }

    @property
    def info_reversed(self):
        owner_color = None
        if self.owner is not None:
            # print("change color")
            if self.owner.color == 'blue':
                owner_color = 'red'
            else:
                owner_color = 'blue'
        direction = self.direction
        if direction is not None:
            direction = (direction + 180) % 360
        return {
            'x': -self.x,
            'y': -self.y,
            'radius': self.radius,
            'owner_color': owner_color,
            'owner_number': None if self.owner is None else self.owner.number,
            'direction': direction,
            'speed': self.speed,
        }
