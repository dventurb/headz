import pygame as pg

from config import WIDTH, HEIGHT

from widgets import Image

class GameMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock 
        self.gameStateManager = gameStateManager
        
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

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            position = self.players["player"]["position"] - (self.player.speed / 10)
            if position <= 0:
                self.players["player"]["position"] = 0
            elif position > 0:
                self.players["player"]["position"] = position
            update_position(self)
        if keys[pg.K_RIGHT]:
            position = self.players["player"]["position"] + (self.player.speed / 10)
            if position >= WIDTH:
                self.players["player"]["position"] = WIDTH
            elif position < WIDTH:
                self.players["player"]["position"] = position
            update_position(self)

    def draw(self):
        self.screen.blit(self.stadium, (0, 0))
    
        self.players["player"]["sprite"].draw(self.screen)
        self.players["opponent"]["sprite"].draw(self.screen)


def update_position(self):
    position = self.players["player"]["position"]

    # TODO: Still need to do position for the jump
    self.players["player"]["sprite"] = Image(self.player.side_right, (position, 800))

        
