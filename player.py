import pygame as pg 

class Player:
    def __init__(self, name: str, sprite: str, font: str, shot: int, jump: int, speed: int):
        self.name = name
        self.sprite = sprite
        self.font = font
        self.shot = shot 
        self.jump = jump 
        self.speed = speed

        self.unlock = False

class PlayerManager:
    def __init__(self):
        self.players = []

    def add_player(self, player: Player):
        self.players.append(player)

    def get_unlock_players(self):
        return [player for player in self.players if player.unlock]

