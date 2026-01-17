import pygame as pg
import cv2

from game import Game, GameStateManager
from config import WIDTH, HEIGHT

class PlayerSelectMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.background = pg.image.load("assets/backgrounds/select_player_menu.png").convert()

        self.play_music = False

    def run(self, events):
        if not self.play_music:
            #pg.mixer.music.load("assets/sounds/loop.mp3")
            #pg.mixer.music.play(-1)
            self.play_music = True

            self.screen.blit(self.background, (0, 0))
        
        self.screen.blit(self.background, (0, 0))

