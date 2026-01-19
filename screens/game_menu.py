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
            
            self.players = {
                "player": Image(self.player.side_right, (384, 800)),
                "opponent": Image(self.opponent.side_left, (1152, 800))
                }

        self.draw()

        if not self.play_music:
            pg.mixer.music.load("assets/sounds/portugal.mp3")
            pg.mixer.music.play(-1)
            self.play_music = True
        

    def draw(self):
        self.screen.blit(self.stadium, (0, 0))

        self.players["player"].draw(self.screen)
        self.players["opponent"].draw(self.screen)


        
