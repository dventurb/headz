import pygame as pg
import cv2

from game import Game, GameStateManager
from config import WIDTH, HEIGHT
from stadium import Stadium, StadiumManager 
from widgets import ButtonImage, Image

class StadiumSelectScreen:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.background = pg.image.load("assets/backgrounds/selection_screen.png").convert()
        
        self.switch_sound = pg.mixer.Sound("assets/sounds/switch.mp3")
        self.click_sound = pg.mixer.Sound("assets/sounds/click.mp3")
        
        self.buttons = {
                "left":  ButtonImage(pg.image.load("assets/buttons/left.png"), (368, 438), click_button_left),
                "right": ButtonImage(pg.image.load("assets/buttons/right.png"), (1040, 438), click_button_right),
                "select": ButtonImage(pg.image.load("assets/buttons/select.png"), (554, 800), click_button_select)
                }
    
        stadiums = [
                Stadium("Portugal", "assets/stadiums/portugal/"),
                Stadium("Mexico", "assets/stadiums/mexico/"),
                Stadium("France", "assets/stadiums/france/")
                ]

        self.stadiumManager = StadiumManager()
        for stadium in stadiums:
            self.stadiumManager.add_stadium(stadium)

        self.current_stadium_index = 0 
        
        self.stadium = Image(self.stadiumManager.stadiums[self.current_stadium_index].flag, (768, 512))


    def run(self, events):
        self.draw()

        for event in events:
            for button in self.buttons.values():
                button.on_click(event, self)

            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    click_button_left(self)
                if event.key == pg.K_RIGHT:
                    click_button_right(self)

        for button in self.buttons.values():
            update_button(self, button)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.stadium.draw(self.screen)
        
        for button in self.buttons.values():
            button.draw(self.screen)


def click_button_left(self):
    self.switch_sound.play()

    self.current_stadium_index = (self.current_stadium_index - 1) % len(self.stadiumManager.stadiums)

    self.stadium = Image(self.stadiumManager.stadiums[self.current_stadium_index].flag, (768, 512))


def click_button_right(self):
    self.switch_sound.play()
    
    self.current_stadium_index = (self.current_stadium_index + 1) % len(self.stadiumManager.stadiums)

    self.stadium = Image(self.stadiumManager.stadiums[self.current_stadium_index].flag, (768, 512))


def click_button_select(self):
    self.click_sound.play()
    
    pg.mixer.music.stop()

    self.gameStateManager.selected_stadium = self.stadiumManager.stadiums[self.current_stadium_index]

    # set screen to game play scene
    self.gameStateManager.set_state("gameplay_screen")

def update_button(self, button):
    button.check_hover()

    if button.hovered == True:
        button.img = button.img_hovered 
    else:
        button.img = button.img_original
