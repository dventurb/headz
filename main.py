import pygame as pg

def main():

    # Initialize pygame 
    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)
    pg.init()
    
    if pg.mixer and not pg.mixer.get_init():
        print("No sound.")
        pg.mixer = None

if __name__ == "__main__":
    main()
    pg.quit()
