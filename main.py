import pygame as pg

from game import initialize_game

WIDTH, HEIGHT = 900, 600

def main():
    pg.mixer.init()
    pg.init()

# Set the display mode
    screen = pg.display.set_mode((WIDTH, HEIGHT))

    initialize_game()


if __name__ == "__main__":
    main()
    pg.quit()
