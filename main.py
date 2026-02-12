import pygame as pg

from game import Game, GameStateManager
from screens import IntroScreen, MainMenu, PlayerSelectMenu, StadiumSelectMenu, GameMenu
from config import WIDTH, HEIGHT

def main():
    pg.mixer.pre_init(44100, -16, 2, 2048)
    pg.init()

    # Set the display mode
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    
    # FPS
    clock = pg.time.Clock()
    clock.tick(50)
   
    # Title 
    pg.display.set_caption("Headz")
    
    game = Game(screen, clock, GameStateManager("intro"))
    
    game.intro = IntroScreen(game.screen, game.clock, game.gameStateManager) 
    game.mainMenu = MainMenu(game.screen, game.clock, game.gameStateManager)
    game.playerSelectMenu = PlayerSelectMenu(game.screen, game.clock, game.gameStateManager)
    game.stadiumSelectMenu = StadiumSelectMenu(game.screen, game.clock, game.gameStateManager)
    game.gameMenu = GameMenu(game.screen, game.clock, game.gameStateManager)

    game.states = {
                "intro": game.intro, 
                "mainMenu": game.mainMenu, 
                "playerSelectMenu": game.playerSelectMenu,
                "stadiumSelectMenu": game.stadiumSelectMenu,
                "gameMenu": game.gameMenu
               }

    game.run()

    pg.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
    pg.quit()
