import pygame as pg

from game import Game, GameStateManager
from screens import IntroScreen, MainScreen, PlayerSelectScreen, StadiumSelectScreen, GameplayScreen
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
    
    game = Game(screen, clock, GameStateManager("intro_screen"))
    
    game.intro_screen = IntroScreen(game.screen, game.clock, game.gameStateManager) 
    game.main_screen = MainScreen(game.screen, game.clock, game.gameStateManager)
    game.player_select_screen = PlayerSelectScreen(game.screen, game.clock, game.gameStateManager)
    game.stadium_select_screen = StadiumSelectScreen(game.screen, game.clock, game.gameStateManager)
    game.gameplay_screen = GameplayScreen(game.screen, game.clock, game.gameStateManager)

    game.states = {
                "intro_screen": game.intro_screen, 
                "main_screen": game.main_screen, 
                "player_select_screen": game.player_select_screen,
                "stadium_select_screen": game.stadium_select_screen,
                "gameplay_screen": game.gameplay_screen
               }

    game.run()

    pg.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
    pg.quit()
