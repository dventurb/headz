import pygame as pg 
import pymunk as pm

from widgets import Image

class Player:
    def __init__(self, path: str, shot: int, jump: int, speed: int):
        self.front = f"{path}front.png"
        self.name =  f"{path}name.png"
        self.side_right = f"{path}side_right.png"
        self.side_left = f"{path}side_left.png"

        self.image = None 

        self.on_pitch = True

        self.shot = shot 
        self.jump = jump 
        self.speed = speed
        
        vs = [(-75, -112), (75, -112), (75, 112), (-75, 112)]
        self.body = pm.Body(5, pm.moment_for_poly(10, vs))
        
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = 0.5
        self.shape.collision_type = 1

    def draw(self, screen):
        self.image.draw(screen)
    
    def update(self):
        self.image.rect.center = self.body.position

    def update_sprite(self, side : str):
        if side == "left":
            self.image = Image(self.side_left, (self.body.position))

        elif side == "right":
            self.image = Image(self.side_right, (self.body.position))

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def get_unlock_players(self):
        return [player for player in self.players]

