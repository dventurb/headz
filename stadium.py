import pygame as pg 
import pymunk as pm

from widgets import Image

class Stadium:
    def __init__(self, name : str, path: str):
        self.name = name 

        self.stadium = f"{path}stadium.png"
        self.flag =  f"{path}flag.png"
        self.sound = f"{path}sound.mp3"

        self.image = None


class StadiumManager:
    def __init__(self):
        self.stadiums = []

    def add_stadium(self, stadium: Stadium):
        self.stadiums.append(stadium)
