import pygame as pg
import math 
from enum import Enum

from config import GRAVITY

class Role(Enum):
    ATTACK = 0
    DEFEND = 1
    NEUTRAL = 2

class Action(Enum):
    JUMP = 0 
    MOVE_LEFT = 1 
    MOVE_RIGHT = 2
    HIGH_KICK = 3
    LOW_KICK = 4
    LIFT_BALL = 5
    PICK_BALL = 6

class UtilityAI:
    def __init__(self):
        self.visited = {}

        self.role = None

    def update(self, ball, player, npc):
        self.role = self.evaluate_role(ball, player, npc)
        self.action = self.evaluate_action(ball, player, npc)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def evaluate_role(self, ball, player, npc):
        player_distance = self.distance(ball.position.x, ball.position.y, player.position.x, player.position.y) 
        npc_distance = self.distance(ball.position.x, ball.position.y, npc.position.x, npc.position.y) 

        if player_distance > npc_distance:
            self.role = Role.ATTACK
        elif npc_distance > player_distance:
            self.role = Role.DEFEND
        else:
            self.role = Role.NEUTRAL

        return self.role

    def evaluate_action(self, ball, player, npc, action):
        utility = 0

        nx, ny = npc.position.x, npc.position.y

        if action == Action.JUMP:
            vy0 = -npc.jump * 10
            
            # h = vy0^2 / 2g
            ymax = (vy0 * vy0) / (2 * GRAVITY)

            distance_x = abs(ball.position.x - npc.position.x)
            distance_y = npc.position.y - ball.position.y

            if npc.on_pitch and distance_y > 0 and distance_y <= ymax and distance_x < 20:
                utility += 120
            else:
                utility -= 60
        
            return utility

        elif action == Action.MOVE_LEFT:
            dx_ball = ball.position.x - npc.position.x 

            if dx_ball < -30:
                utility += 60
            else:
                utility -= 30

            if self.role == Role.ATTACK and dx_ball < 0:
                utility += 40 

            return utility

        elif action == Action.MOVE_RIGHT:
            if ball.position.x > npc.position.x:
                utility += 120
            else:
                utility -= 70

            return utility

    def choose_action(self, ball, player, npc):
        actions = [
                Action.JUMP,
                Action.MOVE_LEFT, 
                Action.MOVE_RIGHT,
                Action.HIGH_KICK,
                Action.LOW_KICK,
                Action.LIFT_BALL,
                Action.PICK_BALL
                ]

        scores = {}

        for action in actions:
            scores[action] = self.evaluate_action(ball, player, npc, action)

        best_score = max(scores, key=socres.get)

        return best_score

    def execute_action(self, npc, space, ball):
        match self.action:
            case Action.JUMP:
                self.jump(npc)
            case Action.MOVE_LEFT:
                self.move_left(npc)
            case Action.MOVE_RIGHT:
                self.move_right(npc)
            case Action.HIGH_KICK:
                self.kick_high(npc, ball)
            case Action.LOW_KICK:
                self.kick_low(npc, ball)
            case Action.PICK_BALL:
                self.pick_ball(npc, space, ball)

    # Movement the NPC
    def move_left(self, npc):
        npc.update_sprite("left")
        npc.body.velocity = (-npc.speed * 5, npc.body.velocity.y)

    def move_right(self, npc):
        npc.update_sprite("right")
        npc.body.velocity = (npc.speed * 5, npc.body.velocity.y)

    def jump(self, npc):
        pg.mixer.Sound("assets/sounds/jump.mp3").play() 
        npc.on_pitch = False
        npc.body.velocity = (npc.body.velocity.x, -npc.jump * 10)

    def pick_ball(self, npc, space, ball):
        npc.has_ball = True
        space.remove(ball.body, ball.shape)

    def kick_low(self, npc, ball):
        if npc.side == "left":
            ball.body.position = npc.body.position - (40, 0)
            ball.body.apply_impulse_at_world_point((-npc.shot * 10, 0), ball.body.position)
        elif npc.side == "right":
            ball.body.position = npc.body.position + (40, 0)
            ball.body.apply_impulse_at_world_point((npc.shot * 10, 0), ball.body.position)         
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()

    def kick_high(self, npc, ball):
        if npc.side == "left":
            ball.body.position = npc.body.position - (40, 0)
            ball.body.apply_impulse_at_world_point((-npc.shot * 5, -300), ball.body.position)
        elif npc.side == "right":
            ball.body.position = npc.body.position + (40, 0)
            ball.body.apply_impulse_at_world_point((npc.shot * 5, -300), ball.body.position)         
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()













