import pygame as pg
import math 
from enum import Enum

from config import WIDTH, HEIGHT, GRAVITY

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
    WAIT = 7

class UtilityAI:
    def __init__(self):
        self.role = Role.ATTACK
        self.action = Action.MOVE_LEFT

    def update(self, ball, player, npc):
        self.role = self.evaluate_role(ball, player, npc)
        self.action = self.choose_action(ball, player, npc)

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def evaluate_role(self, ball, player, npc):
        score = 0 

        player_distance = self.distance(ball.body.position.x, ball.body.position.y, player.body.position.x, player.body.position.y) 
        npc_distance = self.distance(ball.body.position.x, ball.body.position.y, npc.body.position.x, npc.body.position.y) 

        if npc.has_ball:
            score += 100
        elif player.has_ball:
            score -= 100

        score += (player_distance - npc_distance)

        if npc.body.position.x < WIDTH / 2:
            score += 20
        else:
            score -=20
        
        if ball.body_in_space():
            if ball.body.velocity.x < 0:
                score += 20

        if score > 40:
            self.role = Role.ATTACK
        elif score < -40:
            self.role = Role.DEFEND
        else:
            self.role = Role.NEUTRAL 

        return self.role

    def evaluate_action(self, ball, player, npc, action):
        utility = 0
        
        if ball.body_in_space():
            dx_ball = ball.body.position.x - npc.body.position.x 
        elif player.has_ball:
            dx_ball = player.body.position.x - npc.body.position.x 
        else:
            dx_ball = 0
        
        # JUMP 
        if action == Action.JUMP:
            vy0 = -npc.jump * 10
            time_reach = abs(vy0) / GRAVITY
    
            # Predict where the ball is going (y = y0 + v0t - 1/2gt^2) 
            ball_y_future = ball.body.position.y + ball.body.velocity.y * time_reach + 0.5 * GRAVITY * time_reach * time_reach

            npc_y_max = (vy0 * vy0) / (2 * GRAVITY)

            if abs(dx_ball) < 400 and ball_y_future < npc_y_max + 50:
                utility += 140
            else:
                utility -= 100
            
            # NPC already in the air
            if not npc.on_pitch:
                utility -= 200
        
            return utility
        
        # Move Left
        elif action == Action.MOVE_LEFT:
            # Ball on the left of the NPC
            if dx_ball < 0:
                utility += 60
            else:
                utility -= 30

            if self.role == Role.ATTACK and dx_ball < 0:
                utility += 40 

            if self.role == Role.DEFEND and npc.body.position.x > WIDTH / 2:
                utility += 20

            return utility

        # Move Right
        elif action == Action.MOVE_RIGHT:
            if dx_ball > 0 :
                utility += 60
            else:
                utility -= 30

            if self.role == Role.DEFEND:
                utility += 30 

            if self.role == Role.DEFEND and npc.body.position.x < WIDTH / 2: 
                utility += 20 

            return utility

        elif action == Action.PICK_BALL:
            if npc.has_ball:
               return -80 

            d_ball = self.distance(ball.body.position.x, ball.body.position.y, npc.body.position.x, npc.body.position.y) 
            d_player = self.distance(player.body.position.x, player.body.position.y, npc.body.position.x, npc.body.position.y)

            if d_ball < 150 and not player.has_ball:
                utility += 160
            elif d_player < 150 and player.has_ball:
                utility += 140
            else:
                utility -= 80

            if self.role == Role.ATTACK:
                utility += 20

            return utility

        elif action == Action.HIGH_KICK:
            if npc.has_ball:
                # Half pitch
                if npc.body.position.x < (WIDTH / 2): 
                    utility += 120
                else:
                    utility  -= 60

                if player.body.position.x > 100:
                    utility += 60
            else:
                utility -= 80

            return utility

        elif action == Action.WAIT:
            distance_x_to_player = abs(player.body.position.x - npc.body.position.x)

            if player.has_ball and distance_x_to_player < 150: 
                utility += 60 

            if self.role == Role.NEUTRAL:
                utility += 30 

            return utility



    def choose_action(self, ball, player, npc):
        actions = [
                Action.JUMP,
                Action.MOVE_LEFT, 
                Action.MOVE_RIGHT,
                Action.HIGH_KICK,
                #Action.LOW_KICK,
                #Action.LIFT_BALL,
                Action.PICK_BALL,
                Action.WAIT
                ]

        scores = {}

        for action in actions:
            scores[action] = self.evaluate_action(ball, player, npc, action)

        best_score = max(scores, key=scores.get)
        #print(best_score)

        return best_score

    def execute_action(self, ball, npc, space):
        match self.action:
            case Action.JUMP:
                self.jump(npc)
            case Action.MOVE_LEFT:
                self.move_left(npc)
            case Action.MOVE_RIGHT:
                self.move_right(npc)
            case Action.HIGH_KICK:
                self.kick_high(npc, ball, space)
            case Action.LOW_KICK:
                self.kick_low(npc, ball)
            case Action.PICK_BALL:
                self.pick_ball(npc, space, ball)
            case Action.WAIT:
                self.wait(npc)

    # Movement the NPC
    def move_left(self, npc):
        npc.update_sprite("left")
        npc.body.velocity = (-npc.speed * 5, npc.body.velocity.y)

    def move_right(self, npc):
        npc.update_sprite("right")
        npc.body.velocity = (npc.speed * 5, npc.body.velocity.y)

    def jump(self, npc):
        if npc.on_pitch:
            pg.mixer.Sound("assets/sounds/jump.mp3").play() 
            npc.on_pitch = False
            npc.body.velocity = (npc.body.velocity.x, -npc.jump * 10)

    def pick_ball(self, npc, space, ball):
        npc.has_ball = True
        if ball.body_in_space():
            space.remove(ball.body, ball.shape)

    def kick_low(self, npc, ball):
        if npc.side == "left":
            ball.body.position = npc.body.position - (40, 0)
            ball.body.apply_impulse_at_world_point((-npc.shot * 2, 0), ball.body.position)
        elif npc.side == "right":
            ball.body.position = npc.body.position + (40, 0)
            ball.body.apply_impulse_at_world_point((npc.shot * 2, 0), ball.body.position)         
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
        npc.has_ball = False

    def kick_high(self, npc, ball, space):
        if not ball.body_in_space():
            space.add(ball.body, ball.shape)
        if npc.side == "left":
            ball.body.position = npc.body.position - (40, 0)
            ball.body.apply_impulse_at_world_point((-npc.shot * 2, -200), ball.body.position)
        elif npc.side == "right":
            ball.body.position = npc.body.position + (40, 0)
            ball.body.apply_impulse_at_world_point((npc.shot * 2, -200), ball.body.position)         
        pg.mixer.Sound("assets/sounds/ball_kick.mp3").play()
        npc.has_ball = False

    def wait(self, npc):
        npc.update_sprite("left")





