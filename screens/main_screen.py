import pygame as pg
import cv2

from widgets import ButtonImage
from game import Game, GameStateManager
from config import WIDTH, HEIGHT

class MainScreen:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.background = pg.image.load("assets/backgrounds/main_screen.png").convert()

        self.click_sound = pg.mixer.Sound("assets/sounds/click.mp3")

        self.play_music = False

        self.button = ButtonImage(pg.image.load("assets/buttons/start.png").convert_alpha(), (560, 800), click_button_start)

    
    def run(self, events):
        self.draw()

        if not self.play_music:
            pg.mixer.music.load("assets/sounds/loop.mp3")
            pg.mixer.music.play(-1)
            self.play_music = True

        for event in events:
            self.button.on_click(event, self)

        update_button(self.button)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.button.draw(self.screen)


def click_button_start(self):
    self.click_sound.play()

    # Set game state to player_select_screen
    self.gameStateManager.set_state("player_select_screen")


def update_button(button):
    button.check_hover()

    if button.hovered == True:
        button.img = button.img_hovered 
    else:
        button.img = button.img_original
