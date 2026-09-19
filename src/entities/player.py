import pygame as pg 
import pymunk as pm
from enum import Enum

from ui.widgets import Image

class Side(Enum):
    LEFT = 0 
    RIGHT = 1 

    def direction(self):
        return -1 if self == Side.LEFT else 1 

    def offset(self):
        return -40 if self == Side.LEFT else 40 

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
        
        vs = [(-70, -130), (70, -130), (70, 100), (-70, 100)]
        self.body = pm.Body(5, pm.moment_for_poly(5, vs))
        
        self.shape = pm.Poly(self.body, vs)
        self.shape.friction = 0.2
        self.shape.collision_type = 1 # NPC use collision_type number 6

        self.touch_ball = False # Only for NPC

    def draw(self, screen):
        self.image.draw(screen)
    
    def update(self):
        self.image.rect.center = self.body.position

    def update_sprite(self, side : Side):
        if side == Side.LEFT:
            self.side = Side.LEFT
            self.image = Image(self.side_left, (self.body.position))

        elif side == Side.RIGHT:
            self.side = Side.RIGHT
            self.image = Image(self.side_right, (self.body.position))

    def reset_actions(self):
        self.kick_low = False
        self.kick_high = False
        self.lift_ball = False
        self.has_ball = False

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def get_unlock_players(self):
        return [player for player in self.players]

