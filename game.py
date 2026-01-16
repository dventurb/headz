import pygame as pg
import os


def initialize_game():
    sound = pg.mixer.Sound("assets/sounds/loop.mp3")
    while(True):
        sound.play()
