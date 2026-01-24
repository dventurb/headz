import pygame as pg 
import pymunk as pm

from widgets import Image

class Player:
    def __init__(self, name : str, path: str, shot: int, jump: int, speed: int):
        self.name = name 

        self.front = f"{path}front.png"
        self.font =  f"{path}name.png"
        self.side_right = f"{path}side_right.png"
        self.side_left = f"{path}side_left.png"

        self.image = None 

        self.side = None

        self.on_pitch = True
        
        self.kick_low = False
        self.kick_high = False
        self.lift_ball = False
        
        self.has_ball = False

        self.shot = shot 
        self.jump = jump 
        self.speed = speed

        self.score = 0
        
        vs = [(-70, -100), (70, -100), (70, 100), (-70, 100)]
        self.body = pm.Body(5, pm.moment_for_poly(5, vs))
        
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = 0.2
        self.shape.collision_type = 1

    def draw(self, screen):
        self.image.draw(screen)
    
    def update(self):
        self.image.rect.center = self.body.position

    def update_sprite(self, side : str):
        if side == "left":
            self.side = "left"
            self.image = Image(self.side_left, (self.body.position))

        elif side == "right":
            self.side = "right"
            self.image = Image(self.side_right, (self.body.position))

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def get_unlock_players(self):
        return [player for player in self.players]

