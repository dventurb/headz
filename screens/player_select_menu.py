import pygame as pg
import cv2

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
        
        self.buttons = {
                "left":  ButtonImage(pg.image.load("assets/buttons/left.png"), (418, 438), click_button_left),
                "right": ButtonImage(pg.image.load("assets/buttons/right.png"), (990, 438), click_button_right),
                "select": ButtonImage(pg.image.load("assets/buttons/select.png"), (554, 800), click_button_select)
                }
    
        # The next lines of code need a better aproach, I will definitely change this.
        players = [
                Player("Bedas", "assets/characters/bedas.png", "assets/bedas.png", 50, 30, 30),
                Player("Lage", "assets/characters/lage.png", "assets/lage.png", 70, 50, 60),
                Player("João David", "assets/characters/joaodavid.png", "assets/joaodavid.png", 70, 60, 50)
                ]

        self.players = PlayerManager()
        for player in players:
            player.unlock = True
            self.players.add_player(player)

        self.current_player_index = 0 
        
        self.character = {
                "player": self.players.players[self.current_player_index],
                "font": Image(self.players.players[self.current_player_index].font, (768, 200)), 
                "sprite": Image(self.players.players[self.current_player_index].sprite, (768, 512))
                }


    def run(self, events):
        self.draw()

        for event in events:
            self.buttons["left"].on_click(event, self)
            self.buttons["right"].on_click(event, self)

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
    self.current_player_index = (self.current_player_index - 1) % len(self.players.players)

    self.character["player"] = self.players.players[self.current_player_index]
    self.character["font"] = Image(self.players.players[self.current_player_index].font, (768, 200))
    self.character["sprite"] = Image(self.players.players[self.current_player_index].sprite, (768, 512))


def click_button_right(self):
    self.current_player_index = (self.current_player_index + 1) % len(self.players.players)

    self.character["player"] = self.players.players[self.current_player_index]
    self.character["font"] = Image(self.players.players[self.current_player_index].font, (768, 200))
    self.character["sprite"] = Image(self.players.players[self.current_player_index].sprite, (768, 512))


def click_button_select(self):
    test = self.current_player_index


def update_button(self, button):
    button.check_hover()

    if button.hovered == True:
        button.img = button.img_hovered 
    else:
        button.img = button.img_original
