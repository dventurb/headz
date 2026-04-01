import pygame as pg
import cv2
import random

from game import Game, GameStateManager
from config import WIDTH, HEIGHT
from player import Player, PlayerManager 
from widgets import ButtonImage, Image

class PlayerSelectMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.background = pg.image.load("assets/backgrounds/select_player_menu.png").convert()
        
        self.switch_sound = pg.mixer.Sound("assets/sounds/switch.mp3")
        self.start_sound = pg.mixer.Sound("assets/sounds/start.mp3")

        self.buttons = {
                "left":  ButtonImage(pg.image.load("assets/buttons/left.png"), (418, 438), click_button_left),
                "right": ButtonImage(pg.image.load("assets/buttons/right.png"), (990, 438), click_button_right),
                "select": ButtonImage(pg.image.load("assets/buttons/select.png"), (554, 800), click_button_select)
                }
    
        # The next lines of code need a better aproach, I will definitely change this.
        # Player(path : str, shot : int, jump : int, speed : int)
        players = [
                Player("Bedas", "assets/characters/bedas/", 40, 40, 40),
                Player("Lage", "assets/characters/lage/", 60, 50, 50),
                Player("João David", "assets/characters/joaodavid/", 60, 55, 50),
                Player("Valonga", "assets/characters/valonga/", 70, 30, 30),
                Player("Brito", "assets/characters/brito/", 50, 40, 40)
                ]

        self.playerManager = PlayerManager()
        for player in players:
            self.playerManager.add_player(player)

        self.current_player_index = 0 
        
        self.character = {
                "player": self.playerManager.players[self.current_player_index],
                "font": Image(self.playerManager.players[self.current_player_index].font, (768, 200)), 
                "sprite": Image(self.playerManager.players[self.current_player_index].front, (768, 512))
                }


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
        self.character["font"].draw(self.screen)
        self.character["sprite"].draw(self.screen)
        
        for button in self.buttons.values():
            button.draw(self.screen)


def click_button_left(self):
    self.switch_sound.play()

    self.current_player_index = (self.current_player_index - 1) % len(self.playerManager.players)

    self.character["player"] = self.playerManager.players[self.current_player_index]
    self.character["font"] = Image(self.playerManager.players[self.current_player_index].font, (768, 200))
    self.character["sprite"] = Image(self.playerManager.players[self.current_player_index].front, (768, 512))


def click_button_right(self):
    self.switch_sound.play()
    
    self.current_player_index = (self.current_player_index + 1) % len(self.playerManager.players)

    self.character["player"] = self.playerManager.players[self.current_player_index]
    self.character["font"] = Image(self.playerManager.players[self.current_player_index].font, (768, 200))
    self.character["sprite"] = Image(self.playerManager.players[self.current_player_index].front, (768, 512))


def click_button_select(self):
    self.start_sound.play()
    
    self.gameStateManager.selected_player = self.playerManager.players[self.current_player_index]

    opponents = [
            player for player in self.playerManager.players 
            if player != self.gameStateManager.selected_player 
            ]
    self.gameStateManager.npc = random.choice(opponents)
    
    # set screen to stadium select menu.
    self.gameStateManager.set_state("stadiumSelectMenu")


def update_button(self, button):
    button.check_hover()

    if button.hovered == True:
        button.img = button.img_hovered 
    else:
        button.img = button.img_original
