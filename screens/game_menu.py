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
                        "position": [384, 800],
                        "side": "right"
                        },
                    "opponent": {
                        "sprite": Image(self.opponent.side_left, (1152, 800)),
                        "position": [1152, 800],
                        "side": "left"
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
            position = self.players["player"]["position"][0] - (self.player.speed * 0.1)
            if position <= 0:
                self.players["player"]["position"][0] = 0
            elif position > 0:
                self.players["player"]["position"][0] = position
            
            self.players["player"]["side"] = "left"
            update_position(self)
        
        if keys[pg.K_RIGHT]:
            position = self.players["player"]["position"][0] + (self.player.speed * 0.1)
            if position >= WIDTH:
                self.players["player"]["position"][0] = WIDTH
            elif position < WIDTH:
                self.players["player"]["position"][0] = position
            
            self.players["player"]["side"] = "right"
            update_position(self)
        
        # Jump if the Up arrow key is press and the player is on the ground
        if keys[pg.K_UP] and self.players["player"]["position"][1] >= 800: 
            self.players["player"]["position"][1] -= self.player.jump * 2 
            update_position(self)
        
        if keys[pg.K_SPACE] and self.players["player"]["sprite"].rect.colliderect(self.ball["sprite"].rect):    
            if self.players["player"]["side"] == "left":
                self.ball["velocity"][0] = -abs(self.ball["velocity"][0]) * self.player.shot 
                self.ball["position"][0] += self.ball["velocity"][0]
            elif self.players["player"]["side"] == "right":
                self.ball["velocity"][0] = abs(self.ball["velocity"][0]) * self.player.shot
                self.ball["position"][0] += self.ball["velocity"][0]
        
        # If the player jump go to the ground
        if self.players["player"]["position"][1] < 800:
            self.players["player"]["position"][1] += 0.5
            update_position(self)

        # References: https://stackoverflow.com/questions/62998806/how-to-make-a-bouncy-ball-in-pygame-python
        # Ball falling down with bouncy effect
        if self.ball["falldown"]:
            
            # Still falling
            if self.ball["position"][1] < 850:
                self.ball["velocity"][1] += 0.1 # y value 
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
        


        if self.players["player"]["sprite"].rect.colliderect(self.ball["sprite"].rect):    
            print("colide")
            if self.players["player"]["side"] == "left":
                self.ball["velocity"][0] = -abs(self.ball["velocity"][0]) 
                self.ball["position"][0] += self.ball["velocity"][0]
            elif self.players["player"]["side"] == "right":
                self.ball["velocity"][0] = abs(self.ball["velocity"][0]) 
                self.ball["position"][0] += self.ball["velocity"][0]

            # Left wall 
            if self.ball["position"][0] <= 0:
                self.ball["position"][0] = 0
            
            # Right wall
            if self.ball["position"][0] >= WIDTH:
                self.ball["position"][0] = WIDTH


            move_ball(self)
            

    def draw(self):
        self.screen.blit(self.stadium, (0, 0))
    
        self.ball["sprite"].draw(self.screen)

        self.players["player"]["sprite"].draw(self.screen)
        self.players["opponent"]["sprite"].draw(self.screen)


def move_ball(self):
    position = self.ball["position"]

    self.ball["sprite"] = Image("assets/ball/ball.png", (position))

def update_position(self):
    position = self.players["player"]["position"]
    
    # TODO: Still need to do position for the jump
    if self.players["player"]["side"] == "left":
        self.players["player"]["sprite"] = Image(self.player.side_left, (position))

    elif self.players["player"]["side"] == "right":
        self.players["player"]["sprite"] = Image(self.player.side_right, (position))

        
