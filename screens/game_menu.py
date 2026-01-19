import pygame as pg

from config import WIDTH, HEIGHT
from widgets import Image

import random 

class GameMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock 
        self.gameStateManager = gameStateManager
        
        # TODO: The user can select the stadium  
        self.stadium = pg.image.load("assets/stadiums/portugal.png").convert()
        self.stadium = pg.transform.scale(self.stadium, (WIDTH, HEIGHT))

        self.ball = {
                "sprite": Image("assets/ball/ball.png", (768, 100)),
                "position": [768, 100],
                "velocity": [0, 0],
                "falldown": True,
                "bounce": True
                }

        self.player = None
        self.opponent = None

        self.players = {}
 

        self.play_music = False

    def run(self, events):
        if self.player is None or self.opponent is None:
            self.player = self.gameStateManager.selected_player
            self.opponent = self.gameStateManager.opponent
           
           # TODO: Position y for the jump
            self.players = {
                    "player": {
                        "sprite": Image(self.player.side_right, (384, 800)),
                        "position": 384   
                        },
                    "opponent": {
                        "sprite": Image(self.opponent.side_left, (1152, 800)),
                        "position": 1152
                        }
                    }

        self.draw()

        if not self.play_music:
            pg.mixer.music.load("assets/sounds/portugal.mp3")
            pg.mixer.music.play(-1)
            self.play_music = True
       
       # Movement the player
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            position = self.players["player"]["position"] - (self.player.speed * 0.1)
            if position <= 0:
                self.players["player"]["position"] = 0
            elif position > 0:
                self.players["player"]["position"] = position
            update_position(self, self.player.side_left)
        if keys[pg.K_RIGHT]:
            position = self.players["player"]["position"] + (self.player.speed * 0.1)
            if position >= WIDTH:
                self.players["player"]["position"] = WIDTH
            elif position < WIDTH:
                self.players["player"]["position"] = position
            update_position(self, self.player.side_right)
      
        # References: https://stackoverflow.com/questions/62998806/how-to-make-a-bouncy-ball-in-pygame-python
        # Ball falling down with bouncy effect
        if self.ball["falldown"]:
            
            # Still falling
            if self.ball["position"][1] < 850:
                self.ball["velocity"][1] += 0.2 # y value 
                self.ball["velocity"][0] = random.choice([self.ball["velocity"][0] + 0.02, self.ball["velocity"][0] - 0.02]) # Random select the x value (side where the ball will land)

                self.ball["position"][1] += self.ball["velocity"][1]
                self.ball["position"][0] += self.ball["velocity"][0]

                print("Falling:")
                print(f"Velocity: {self.ball["velocity"][1]}")
                print(f"Positon: {self.ball["position"][1]}")
                move_ball(self)
            
            # Hit the ground
            else:
                # Create a bouncy effect
                if self.ball["velocity"][1] > 0:
                    print()
                    print("Hit the ground")
                    pg.mixer.Sound("assets/sounds/ball_drop.mp3").play()
                    self.ball["velocity"][1] *= -0.9
                    self.ball["position"][1] += self.ball["velocity"][1]
                else:
                    self.ball["falldown"] = False

                move_ball(self)
        
        # Left wall 
        if self.ball["position"][0] <= 0:
            self.ball["velocity"][0] = abs(self.ball["velocity"][0])
        
        # Right wall
        if self.ball["position"][0] >= WIDTH:
            self.ball["velocity"][0] = -abs(self.ball["velocity"][0])


    def draw(self):
        self.screen.blit(self.stadium, (0, 0))
    
        self.ball["sprite"].draw(self.screen)

        self.players["player"]["sprite"].draw(self.screen)
        self.players["opponent"]["sprite"].draw(self.screen)


def move_ball(self):
    position = self.ball["position"]

    self.ball["sprite"] = Image("assets/ball/ball.png", (position))

def update_position(self, side_view):
    position = self.players["player"]["position"]

    # TODO: Still need to do position for the jump
    self.players["player"]["sprite"] = Image(side_view, (position, 800))

        
