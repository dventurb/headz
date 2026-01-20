import pygame as pg
import pymunk as pm 
import random 

from config import WIDTH, HEIGHT
from widgets import Image
from ball import Ball
from pitch import Pitch

class GameMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock 
        self.gameStateManager = gameStateManager
        
        self.space = pm.Space()
        self.space.gravity = 0, 1000

        self.ball = Ball(self.space, "assets/ball/ball.png", (768, 100))
        self.pitch = Pitch(self.space)
        
        # TODO: The user can select the stadium  
        self.stadium = pg.image.load("assets/stadiums/portugal.png").convert()
        self.stadium = pg.transform.scale(self.stadium, (WIDTH, HEIGHT))

        self.player = None
        self.opponent = None

        self.players = {}
 
        self.play_music = False

    def run(self, events):
        if self.player is None or self.opponent is None:
            self.player = self.gameStateManager.selected_player
            self.player.image = Image(self.player.side_right, (384, 760))
            self.player.body.position = (384, 760)

            self.opponent = self.gameStateManager.opponent
            self.opponent.image = Image(self.opponent.side_left, (384, 760))
            self.opponent.body.position = (1152, 760)
            
            self.space.add(self.player.body, self.player.shape)
            self.space.add(self.opponent.body, self.opponent.shape)

        if not self.play_music:
            pg.mixer.music.load("assets/sounds/portugal.mp3")
            pg.mixer.music.play(-1)
            self.play_music = True
        
        self.space.step(1/60)
        self.space.on_collision(2, 3, begin=ball_hits_pitch, data=self.ball)
        self.space.on_collision(1, 3, begin=player_on_pitch, data=self.player)
        
        self.draw()

      # Movement the player
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: 
            self.player.update_sprite("left")
            self.player.body.velocity = (-self.player.speed * 10, self.player.body.velocity.y)
        if keys[pg.K_RIGHT]:
            self.player.update_sprite("right")
            self.player.body.velocity = (self.player.speed * 10, self.player.body.velocity.y)
        if keys[pg.K_UP] and self.player.on_pitch:
            self.player.on_pitch = False
            self.player.body.velocity = (self.player.body.velocity.x, -self.player.jump * 10)


    def draw(self):
        self.screen.blit(self.stadium, (0, 0))
        
        self.ball.update()
        self.ball.draw(self.screen)

        self.player.update()
        self.player.draw(self.screen)
        self.opponent.update()
        self.opponent.draw(self.screen)


def ball_hits_pitch(arbiter, space, data):
    pg.mixer.Sound("assets/sounds/ball_drop.mp3").play()
    
    data.body.velocity = (random.choice([50, -50]), data.body.velocity.y)
    return True

def player_on_pitch(arbiter, space, data):
    data.on_pitch = True
    return True

