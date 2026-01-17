import pygame as pg

from game import initialize_game

WIDTH, HEIGHT = 1536, 1024

def main():
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()

    # Set the display mode
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    # Title 
    pg.display.set_caption("Headz")

    initialize_game(screen)


if __name__ == "__main__":
    main()
    pg.quit()
