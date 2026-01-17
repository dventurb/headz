import pygame as pg
from os import sys
import cv2

from widgets import ButtonImage

WIDTH, HEIGHT = 1536, 1024

def initialize_game(screen):
   
    # Intro video
    # References: https://stackoverflow.com/questions/21356439/how-to-load-and-play-a-video-in-pygame
    video = cv2.VideoCapture("assets/video.mp4")
    video_play, video_image = video.read()

    if not video_play:
        print("Warning, can't load the video.")
        sys.exit(1)

    fps = video.get(cv2.CAP_PROP_FPS)

    clock = pg.time.Clock()

    running = True
    music_play = False
   
    # Play intro sound effect
    pg.mixer.music.load("assets/sounds/intro.mp3")
    pg.mixer.music.play(1)
    
    while running:
        clock.tick(fps)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
        video_play, video_image = video.read()

        if video_play:
            video_surf = pg.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            video_surf = pg.transform.scale(video_surf, (WIDTH, HEIGHT))
            screen.blit(video_surf, (0, 0))
        else:
            if not music_play:
                pg.mixer.music.load("assets/sounds/loop.mp3")
                pg.mixer.music.play(-1) 
                music_play = True

                background = pg.image.load("assets/background.png").convert()
                screen.blit(background, (0, 0))

                btn_start = ButtonImage(pg.image.load("assets/buttons/start.png").convert_alpha(), (560, 800), click_btn)

                btn_start.draw(screen)

            btn_start.on_click(event)

        pg.display.flip()



def click_btn():
    print("click")

