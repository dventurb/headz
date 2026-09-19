import pygame as pg 
import pymunk as pm
import random

from ui.widgets import Image

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

    def body_in_space(self):
        if any(self.shape.space is not None for shape in self.body.shapes):
            return True
        else:
            return False

