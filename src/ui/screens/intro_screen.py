import pygame as pg
from os import sys
import cv2

from core.game import Game, GameStateManager
from core.config import WIDTH, HEIGHT

class IntroScreen:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen 
        self.clock = clock
        self.gameStateManager = gameStateManager 

        self.video = cv2.VideoCapture("assets/videos/video.mp4") 
        self.music = pg.mixer.Sound("assets/sounds/intro.mp3")

    def run(self, events):
        # References: https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame
        video_play, video_image = self.video.read()

        if not video_play:
            print("Warning, can't load the video.")
            sys.exit(1)

        # Play intro sound effect
        self.music.play()

        while video_play:
            video_surf = pg.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            video_surf = pg.transform.scale(video_surf, (WIDTH, HEIGHT))
            
            self.screen.blit(video_surf, (0, 0))

            video_play, video_image = self.video.read()

            pg.display.flip()


        self.video.release()
        
        # End of the intro_screen, set to main screen
        self.gameStateManager.set_state("main_screen")
