import pygame as pg 

class Game:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen
        self.clock = clock 
        self.gameStateManager = gameStateManager

        self.intro = None
        self.mainMenu = None
        self.playerSelectMenu = None 
        self.stadiumSelectMenu = None
        self.gameMenu = None

        self.states = {}

    def run(self):
        running = True
        while running:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    running = False

            self.states[self.gameStateManager.get_state()].run(events)
            
            pg.display.update()


class GameStateManager:
    def __init__(self, current_state):
        self.current_state = current_state

        self.selected_player = None
        self.npc = None
        self.selected_stadium = None

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state

