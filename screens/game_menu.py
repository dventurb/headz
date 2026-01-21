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
        self.space.gravity = 0, 900

        self.ball = Ball(self.space, "assets/ball/ball.png", (768, 100))
        self.pitch = Pitch(self.space)
        
        # TODO: The user can select the stadium  
        self.stadium = pg.image.load("assets/stadiums/portugal.png").convert()
        self.stadium = pg.transform.scale(self.stadium, (WIDTH, HEIGHT))

        self.player = None
        self.opponent = None

        self.players = {}

        self.player_with_ball = None
 
        self.play_music = False

    def run(self, events):
        if self.player is None or self.opponent is None:
            self.player = self.gameStateManager.selected_player
            self.player.image = Image(self.player.side_right, (384, 760))
            self.player.side = "right"
            self.player.body.position = (384, 760)

            self.opponent = self.gameStateManager.opponent
            self.opponent.image = Image(self.opponent.side_left, (384, 760))
            self.player.side = "left"
            self.opponent.body.position = (1152, 760)
            self.opponent.collision_type = 0
            
            self.space.add(self.player.body, self.player.shape)
            self.space.add(self.opponent.body, self.opponent.shape)

        if not self.play_music:
            pg.mixer.music.load("assets/sounds/portugal.mp3")
            pg.mixer.music.play(-1)
            self.play_music = True
        
        self.space.step(1/60)
        
        self.space.on_collision(2, 3, begin=ball_hits_pitch, data=self.ball)
        self.space.on_collision(1, 2, begin=player_with_ball, data=self)
        self.space.on_collision(1, 3, begin=player_on_pitch, data=self.player)
        self.space.on_collision(2, 4, begin=npc_score_goal, data=self)
        self.space.on_collision(2, 5, begin=player_score_goal, data=self)
        
        self.draw()

      # Movement the player
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]: 
            self.player.update_sprite("left")
            self.player.body.velocity = (-self.player.speed * 5, self.player.body.velocity.y)
        if keys[pg.K_RIGHT]:
            self.player.update_sprite("right")
            self.player.body.velocity = (self.player.speed * 5, self.player.body.velocity.y)
        if keys[pg.K_UP] and self.player.on_pitch:
            pg.mixer.Sound("assets/sounds/jump.mp3").play() 
            self.player.on_pitch = False
            self.player.body.velocity = (self.player.body.velocity.x, -self.player.jump * 10)    
    
        # Check when z, x, c keys was pressed (KEYDOWN) and released (KEYUP)
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    self.player.kick_low = True
                if event.key == pg.K_x:
                    self.player.kick_high = True
                if event.key == pg.K_c:
                    self.player.pick_ball = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    self.player.kick_low = False
                if event.key == pg.K_x:
                    self.player.kick_high = False
                if event.key == pg.K_c:
                    self.player.pick_ball = False
        
        # Remove the anchor point from ball and player 
        if not self.player.pick_ball and self.player_with_ball is not None:
            self.space.remove(self.player_with_ball)
            self.player_with_ball = None


        # TODO: First do the goal score 
        if self.ball.body.position.y > HEIGHT:
            self.ball.body.position = (max(min(self.ball.body.position.x, (HEIGHT - 50)), 50), 100)


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
    data.body.velocity = (random.choice([100, -100]), data.body.velocity.y)
    return True

def player_with_ball(arbiter, space, data):
    if data.player.kick_low:
        if data.player.pick_ball and data.player_with_ball is not None:
            data.space.remove(data.player_with_ball)
            data.player_with_ball = None
            data.player.pick_ball = False
       
        if data.player.side == "left":
            data.ball.body.apply_impulse_at_local_point((data.player.shot * 10, 0))
        
        elif data.player.side == "right":
            data.ball.body.apply_impulse_at_local_point((-data.player.shot * 10, 0))
        
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
    
    elif data.player.kick_high:
        if data.player.pick_ball and data.player_with_ball is not None:
            data.space.remove(data.player_with_ball)
            data.player_with_ball = None
            data.player.pick_ball = False

        if data.player.side == "left":
            data.ball.body.apply_impulse_at_local_point((data.player.shot * 10, -300))
        
        elif data.player.side == "right":
            data.ball.body.apply_impulse_at_local_point((-data.player.shot * 10, -300))             
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()

    elif data.player.pick_ball and data.player_with_ball is None:
        if data.player.side == "left":
            data.player_with_ball = pm.constraints.PinJoint(data.player.body, data.ball.body, (0, 0), (0, 0))
        
        elif data.player.side == "right":
            data.player_with_ball = pm.constraints.PinJoint(data.player.body, data.ball.body, (0, 0), (0, 0))
        data.space.add(data.player_with_ball)

    return True


def player_on_pitch(arbiter, space, data):
    data.on_pitch = True
    return True

def npc_score_goal(arbiter, space, data):        
    pg.mixer.Sound("assets/sounds/goal.mp3").play()
    data.opponent.score += 1
    return False

def player_score_goal(arbiter, space, data):
    pg.mixer.Sound("assets/sounds/goal.mp3").play()
    data.player.score += 1
    return False

