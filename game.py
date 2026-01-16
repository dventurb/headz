import pygame as pg
import os


def initialize_game():
    pg.mixer.music.load("assets/sounds/loop.mp3")
    pg.mixer.music.play(-1)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                runnning = false
