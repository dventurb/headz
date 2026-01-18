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
                "right": ButtonImage(pg.image.load("assets/buttons/right.png"), (990, 438), click_button_right)
                }

        players = [
                Player("Bedas", "assets/characters/bedas.png", 50, 30, 30),
                Player("Lage", "assets/characters/lage.png", 70, 50, 60),
                Player("João David", "assets/characters/joaodavid.png", 70, 60, 50)
                ]

        self.players = PlayerManager()
        for player in players:
            player.unlock = True
            self.players.add_player(player)

        self.character = {
                "player": self.players.players[0],
                "font": Image("assets/bedas.png", (768, 200)), 
                "sprite": Image(self.players.players[0].image, (768, 512))
                }

    def run(self, events):
        self.draw()

        for event in events:
            self.buttons["left"].on_click(event, None)
            self.buttons["right"].on_click(event, None)

        update_button(self, self.buttons["left"])
        update_button(self, self.buttons["right"])

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.character["font"].draw(self.screen)
        self.character["sprite"].draw(self.screen)
        
        self.buttons["left"].draw(self.screen)
        self.buttons["right"].draw(self.screen)


def load_players_sprites(screen, players):
    sprites = pg.image.load(player.image).convert_alpha()


def click_button_left(self):
    print("click")

def click_button_right(self):
    print("click")

def update_button(self, button):
    button.check_hover()

    if button.hovered == True:
        button.img = button.img_hovered 
    else:
        button.img = button.img_original
