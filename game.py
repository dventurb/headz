import pygame as pg 

class Game:
    def __init__(self, screen, clock, gameStateManager):
        self.screen = screen
        self.clock = clock 
        self.gameStateManager = gameStateManager

        self.intro = None
        self.mainMenu = None
        #self.playerSelectMenu = None 
        #self.gameMenu = None

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
            self.clock.tick


class GameStateManager:
    def __init__(self, currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

