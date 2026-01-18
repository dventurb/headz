import pygame as pg
import cv2

from game import Game, GameStateManager
from config import WIDTH, HEIGHT
from player import Player, PlayerManager 
from widgets import ButtonImage

class PlayerSelectMenu:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.background = pg.image.load("assets/backgrounds/select_player_menu.png").convert()

    def run(self, events):

        self.screen.blit(self.background, (0, 0))

        players = [
                Player("Bedas", "assets/characters/bedas.png", 50, 30, 30),
                Player("Lage", "assets/characters/lage.png", 70, 50, 60),
                Player("João David", "assets/characters/joaodavid.png", 70, 60, 50)
                   ]

        self.players = PlayerManager()
        for player in players:
            player.unlock = True
            self.players.add_player(player)

        pg.font.init()
        my_font = pg.font.Font("assets/fonts/Crashcourse.ttf", 180)
        label = my_font.render(self.players.players[0].name.upper(), True, (255, 179, 67))
        rect = label.get_rect(center=(768, 200))
        self.screen.blit(label, rect)

        # Left Button
        btn_left = ButtonImage(pg.image.load("assets/buttons/left.png").convert_alpha(), (418, 438), click_button_left)
        btn_left.img = pg.transform.scale(btn_left.img, (128, 147))
        btn_left.draw(self.screen)
        
        # Character Sprite
        sprite = pg.image.load(self.players.players[0].image).convert_alpha()
        self.screen.blit(sprite, sprite.get_rect(topleft=(618, 301)))
        
        # Right Button
        btn_right = ButtonImage(pg.image.load("assets/buttons/right.png").convert_alpha(), (990, 438), click_button_left)
        btn_right.img = pg.transform.scale(btn_right.img, (128, 147))
        btn_right.draw(self.screen)
    

def load_players_sprites(screen, players):
    sprites = pg.image.load(player.image).convert_alpha()


def click_button_left(self):
    print("click")
