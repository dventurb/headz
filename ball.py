import pygame as pg 
import pymunk as pm

from widgets import Image

class Ball:
    def __init__(self, space, path : str, position):
        self.image = Image(path, position)
        self.radius = self.image.image.get_width() / 2

        self.body = pm.Body(0.5, pm.moment_for_circle(0.5, 0, self.radius))
        self.body.position = position

        self.shape = pm.Circle(self.body, self.radius)
        self.shape.elasticity = 1
        self.shape.friction = 0.65
        self.shape.collision_type = 2

        space.add(self.body, self.shape) 

    def draw(self, screen):
        self.image.draw(screen)

    def update(self):
        self.image.rect.center = self.body.position


