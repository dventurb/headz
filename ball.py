import pygame as pg 
import pymunk as pm
import random

from widgets import Image

class Ball:
    def __init__(self, space, path : str, position):
        self.image = Image(path, position)
        self.radius = 16 # by eye

        self.touch = False

        self.body = pm.Body(0.5, pm.moment_for_circle(0.5, 0, self.radius))
        self.body.position = position

        self.shape = pm.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        self.shape.friction = 0.5
        self.shape.collision_type = 2

        space.add(self.body, self.shape) 

    def draw(self, screen):
        self.image.draw(screen)

    def update(self):
        self.image.rect.center = self.body.position

    def update_sprite(self, num : int):
        path = f"assets/ball/ball_{num}.png"
        self.image = Image(path, (self.body.position))

